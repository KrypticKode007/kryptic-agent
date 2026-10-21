import time
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.hmac import HMAC
import os

def accelerated_swmp_verify_and_decrypt(encrypted_weights, key, hmac_key, signature):
    # Ensure performance timing is calculated in nanoseconds
    start_time = time.perf_counter_ns()
    
    # 1. Hardware Accelerated HMAC Verification
    h = HMAC(hmac_key, SHA256())
    h.update(encrypted_weights)
    h.verify(signature) # Throws exception if signature is altered
    
    # 2. Hardware Accelerated AES-256-CTR / CBC Decryption
    # OpenSSL automatically hooks ARMv8 Crypto Extensions on Jetson architectures
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
    
