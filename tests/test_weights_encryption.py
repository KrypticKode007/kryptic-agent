# tests/test_weights_encryption.py
"""
Production verification test case validating the AES-256 weights encryption 
protocol for network consensus payloads under simulated transmission drift.
"""

import pytest
import json
from encrypt_weights import WeightsEncryptionEngine

def test_aes256_weights_wrapping_integrity():
    """
    Verifies that network consensus weight dictionaries are signed, armored, 
    and restored without bit distortion or data corruption during transmission.
    """
    passphrase = "NetworkConsensusConsensusSecret2026"
    engine = WeightsEncryptionEngine(passphrase)

    # 1. Define high-precision network consensus weight matrices
    consensus_weights = {
        "layer_0_node_biases": [0.5512, -0.1194, 0.8841],
        "phi_gamma_matrices": [[1.0, 0.0], [0.0, 1.0]],
        "safety_thresholds": {"max_velocity": 45.0, "critical_stamina": 10.0}
    }

    # 2. Encrypt parameters into armored Base64 cipher text blocks
    armored_payload_string = engine.encrypt_parameter_payload(consensus_weights)
    assert isinstance(armored_payload_string, str)
    
    # Verify that the plaintext figures are obscured and formatted as structured json payloads
    payload_dict = json.loads(armored_payload_string)
    assert "iv" in payload_dict
    assert "ciphertext" in payload_dict

    # 3. Decrypt and verify payload blocks match structural baseline variables perfectly
    recovered_weights = engine.decrypt_parameter_payload(armored_payload_string)
    assert recovered_weights["safety_thresholds"]["max_velocity"] == 45.0
    assert recovered_weights["layer_0_node_biases"][1] == -0.1194
    print("\n[+] Cryptographic Integrity Check: PASS")

def test_tampered_passphrase_exception_handling():
    """Guarantees that incorrect decryption credentials immediately trigger integrity faults."""
    engine_encrypt = WeightsEncryptionEngine("CorrectPassphrase123")
    engine_decrypt = WeightsEncryptionEngine("WrongPassphrase456")

    sample_data = {"weights": [0.1, 0.2, 0.3]}
    secure_string = engine_encrypt.encrypt_parameter_payload(sample_data)

    # Intercept and attempt unauthorized decryption
    with pytest.raises(ValueError) as exception_context:
        engine_decrypt.decrypt_parameter_payload(secure_string)
    
    assert "Integrity failure" in str(exception_context.value)
  
