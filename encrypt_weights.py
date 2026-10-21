#!/usr/bin/env python3
"""
encrypt_weights.py
Automated AES-256 weights encryption protocol for network consensus payloads.
Secures parameter arrays and runtime model configurations using an explicit PBKDF2
derivation matrix before streaming configurations out over active deployment pipelines.
"""

import os
import sys
import json
import base64
from typing import Dict, Any

try:
    from Crypto.Cipher import AES
    from Crypto.Hash import SHA256
    from Crypto.Protocol.KDF import PBKDF2
    from Crypto.Random import get_random_bytes
except ImportError as import_error:
    raise ImportError(
        "encrypt_weights requires PyCryptodome; install it with 'python -m pip install pycryptodome'."
    ) from import_error

class WeightsEncryptionEngine:
    """Provides high-precision symmetric data wrapping boundaries for structural model weights."""
    def __init__(self, passphrase: str):
        self.passphrase = passphrase.encode("utf-8")

    def _derive_crypto_keys(self, salt: bytes) -> bytes:
        """Derives a cryptographically strong 256-bit symmetric block encryption key."""
        return PBKDF2(
            self.passphrase,
            salt,
            dkLen=32,
            count=210_000,
            hmac_hash_module=SHA256,
        )

    def encrypt_parameter_payload(self, weights_dict: Dict[str, Any]) -> str:
        """Serializes model weight parameters and signs them into armored AES-256 blocks."""
        salt = get_random_bytes(16)
        secret_key = self._derive_crypto_keys(salt)
        serialized_data = json.dumps(weights_dict, sort_keys=True).encode("utf-8")

        cipher = AES.new(secret_key, AES.MODE_GCM)
        encrypted_blocks, tag = cipher.encrypt_and_digest(serialized_data)

        armored_payload = {
            "salt": base64.b64encode(salt).decode("utf-8"),
            "iv": base64.b64encode(cipher.nonce).decode("utf-8"),
            "ciphertext": base64.b64encode(encrypted_blocks).decode("utf-8"),
            "tag": base64.b64encode(tag).decode("utf-8"),
        }
        return json.dumps(armored_payload)

    def decrypt_parameter_payload(self, raw_payload: str) -> Dict[str, Any]:
        """Decrypts armored payload objects back into clean parameter registers."""
        try:
            payload = json.loads(raw_payload)
            salt = base64.b64decode(payload["salt"], validate=True)
            iv = base64.b64decode(payload["iv"], validate=True)
            ciphertext = base64.b64decode(payload["ciphertext"], validate=True)
            tag = base64.b64decode(payload["tag"], validate=True)

            secret_key = self._derive_crypto_keys(salt)
            cipher = AES.new(secret_key, AES.MODE_GCM, nonce=iv)
            decrypted_raw = cipher.decrypt_and_verify(ciphertext, tag)

            return json.loads(decrypted_raw.decode("utf-8"))
        except Exception as encryption_err:
            raise ValueError("Integrity failure: Invalid passphrase signatures or broken data blocks.") from encryption_err

# =====================================================================
# SYSTEM VERIFICATION COMPLIANCE WINDOW
# =====================================================================
if __name__ == "__main__":
    print("=" * 70)
    print("⚡ KRYPTIC CRYPTOGRAPHIC CORE: VERIFYING AES-256 WEIGHTS WRAPPING")
    print("=" * 70)
    
    # Mock system metrics configuration definitions
    sample_weights = {
        "layer_0_biases": [0.1248, -0.9854, 0.4412],
        "phi_gamma_matrices": [[0.9, 0.1], [0.0, 1.0]],
        "hardware_bounds": {"max_velocity": 45.0, "stamina_cap": 50.0}
    }
    
    test_phrase = "SystemHomeostasisSecretCoreSignature2026"
    engine = WeightsEncryptionEngine(test_phrase)
    
    print("[*] Encrypting structural model tracking parameters...")
    secure_string = engine.encrypt_parameter_payload(sample_weights)
    print(f"[+] Armored Payload Encoded Digest (Truncated):\n    {secure_string[:90]}...")
    
    print("[*] Executing test decryption sequence...")
    recovered_data = engine.decrypt_parameter_payload(secure_string)
    print(f"[+] Verification Status: PASS. Recovered Bounds: {recovered_data['hardware_bounds']}")
    print("=" * 70)
  
