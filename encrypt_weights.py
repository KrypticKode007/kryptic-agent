import base64
import hashlib
import json
import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


class WeightsEncryptionEngine:
    def __init__(self, passphrase: str):
        self.passphrase = passphrase
        self._key = hashlib.sha256(passphrase.encode("utf-8")).digest()

    def encrypt_parameter_payload(self, payload):
        nonce = os.urandom(12)
        plaintext = json.dumps(payload, sort_keys=True).encode("utf-8")
        encrypted = AESGCM(self._key).encrypt(nonce, plaintext, None)
        ciphertext = encrypted[:-16]
        tag = encrypted[-16:]

        return json.dumps({
            "salt": base64.b64encode(os.urandom(16)).decode("utf-8"),
            "iv": base64.b64encode(nonce).decode("utf-8"),
            "ciphertext": base64.b64encode(ciphertext).decode("utf-8"),
            "tag": base64.b64encode(tag).decode("utf-8"),
        })

    def decrypt_parameter_payload(self, payload_string):
        payload = json.loads(payload_string)
        nonce = base64.b64decode(payload["iv"])
        ciphertext = base64.b64decode(payload["ciphertext"])
        tag = base64.b64decode(payload["tag"])

        try:
            plaintext = AESGCM(self._key).decrypt(nonce, ciphertext + tag, None)
        except Exception as exc:
            raise ValueError("Integrity failure: authentication failed") from exc

        return json.loads(plaintext.decode("utf-8"))
