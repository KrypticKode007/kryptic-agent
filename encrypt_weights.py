import base64
import hashlib
import json
import os
import time
from typing import Any, Dict, Union

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.hmac import HMAC


class WeightsEncryptionEngine:
    """AES-GCM encryption wrapper for model parameter payloads."""

    def __init__(self, passphrase: str):
        self.passphrase = passphrase
        self._key = hashlib.sha256(passphrase.encode("utf-8")).digest()

    def encrypt_parameter_payload(self, payload: Dict[str, Any]) -> str:
        nonce = os.urandom(12)
        plaintext = json.dumps(payload, sort_keys=True).encode("utf-8")
        ciphertext_and_tag = AESGCM(self._key).encrypt(nonce, plaintext, None)
        ciphertext = ciphertext_and_tag[:-16]
        tag = ciphertext_and_tag[-16:]

        return json.dumps(
            {
                "salt": base64.b64encode(os.urandom(16)).decode("utf-8"),
                "iv": base64.b64encode(nonce).decode("utf-8"),
                "ciphertext": base64.b64encode(ciphertext).decode("utf-8"),
                "tag": base64.b64encode(tag).decode("utf-8"),
            },
            sort_keys=True,
        )

    def decrypt_parameter_payload(self, payload_string: Union[str, bytes]) -> Dict[str, Any]:
        if isinstance(payload_string, (bytes, bytearray)):
            payload_string = payload_string.decode("utf-8")

        payload = json.loads(payload_string)
        nonce = base64.b64decode(payload["iv"])
        ciphertext = base64.b64decode(payload["ciphertext"])
        tag = base64.b64decode(payload["tag"])

        try:
            plaintext = AESGCM(self._key).decrypt(nonce, ciphertext + tag, None)
        except Exception as exc:  # pragma: no cover - defensive against tampering
            raise ValueError("Integrity failure: authentication failed") from exc

        return json.loads(plaintext.decode("utf-8"))


def accelerated_swmp_verify_and_decrypt(encrypted_weights, key, hmac_key, signature):
    """Legacy compatibility wrapper matching the repository's original low-level API."""
    start_time = time.perf_counter_ns()

    h = HMAC(hmac_key, hashes.SHA256())
    h.update(encrypted_weights)
    h.verify(signature)

    nonce = encrypted_weights[:16]
    cipher_payload = encrypted_weights[16:]
    cipher = Cipher(algorithms.AES(key), modes.CTR(nonce))
    decryptor = cipher.decryptor()
    decrypted_weights = decryptor.update(cipher_payload) + decryptor.finalize()

    end_time = time.perf_counter_ns()
    total_jitter_ms = (end_time - start_time) / 1_000_000
    print(f"[SWMP HW ACCEL] Decryption and Verification Finished.")
    print(f"[SWMP PERFORMANCE] Total Jitter Footprint: {total_jitter_ms:.4f} ms")
    return decrypted_weights
