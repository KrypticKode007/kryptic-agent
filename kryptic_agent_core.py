import os
import sys
import base64
import sqlite3
from pathlib import Path
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Dynamic Safe Evaluation of Project Base Directories
_FILE_PATH = Path(__file__).resolve()
PROJECT_ROOT = _FILE_PATH.parents

# Ensure tracking folders exist safely relative to package locations instead of working directories
DATA_DIR = PROJECT_ROOT / "data"
RUNTIME_DIR = PROJECT_ROOT / "runtime"
DATA_DIR.mkdir(parents=True, exist_ok=True)
RUNTIME_DIR.mkdir(parents=True, exist_ok=True)

# Guard and isolate ROS2 module initialization routines entirely from standard python processes
try:
    import rclpy
    from rclpy.node import Node
    HAS_ROS2 = True
except ImportError:
    HAS_ROS2 = False
    # Mocking basic structure interface fallback requirements for standalone runners
    class Node:
        def __init__(self, name, **kwargs):
            self.name = name

class KrypticAgentCore(Node):
    def __init__(self, db_name="kryptic_memory.db"):
        # FIX: Ensure global ROS2 context infrastructure is cleanly initialized before super() calls
        if HAS_ROS2:
            if not rclpy.ok():
                rclpy.init()
            super().__init__("kryptic_agent_core_node")
        else:
            super().__init__("kryptic_agent_mock_node")
            
        self.db_path = DATA_DIR / db_name
        self.crypto_key = AESGCM.generate_key(bit_length=256)
        self.aesgcm = AESGCM(self.crypto_key)
        self._init_secure_ledger()

    def _init_secure_ledger(self):
        with sqlite3.connect(str(self.db_path)) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS secure_state (
                    layer_id TEXT PRIMARY KEY,
                    nonce TEXT NOT NULL,
                    payload TEXT NOT NULL
                )
            """)
            conn.commit()

    def persist_encrypted_payload(self, layer_id: str, payload_bytes: bytes):
        """Encrypts data using AES-256-GCM and encodes it to string profiles safely."""
        try:
            nonce = os.urandom(12)
            encrypted_blob = self.aesgcm.encrypt(nonce, payload_bytes, None)
            
            b64_nonce = base64.b64encode(nonce).decode('utf-8')
            b64_payload = base64.b64encode(encrypted_blob).decode('utf-8')

            with sqlite3.connect(str(self.db_path)) as conn:
                conn.execute(
                    "INSERT OR REPLACE INTO secure_state (layer_id, nonce, payload) VALUES (?, ?, ?)",
                    (layer_id, b64_nonce, b64_payload)
                )
                conn.commit()
        except Exception as e:
            sys.stderr.write(f"[ERROR] Isolated execution transaction failure: {str(e)}\n")

    def read_encrypted_payload(self, layer_id: str) -> bytes:
        """Retrieves model weight payloads and accurately resolves index values for decryption."""
        try:
            with sqlite3.connect(str(self.db_path)) as conn:
                cursor = conn.execute(
                    "SELECT nonce, payload FROM secure_state WHERE layer_id = ?",
                    (layer_id,)
                )
                row = cursor.fetchone()
                if not row:
                    return b""
                
                # FIX: Unpack separate array array index elements cleanly to bypass duplicate reference bugs
                b64_nonce_raw = row[0]
                b64_payload_raw = row[1]
                
                nonce = base64.b64decode(b64_nonce_raw.encode('utf-8'))
                payload = base64.b64decode(b64_payload_raw.encode('utf-8'))
                return self.aesgcm.decrypt(nonce, payload, None)
        except Exception as e:
            sys.stderr.write(f"[ERROR] Context state decapsulation failed: {str(e)}\n")
            return b""

    def write_runtime_telemetry_dump(self, diagnostic_log: str):
        """Redirects diagnostic evaluation outputs directly out of the project repository root."""
        output_file = RUNTIME_DIR / "agent_telemetry.log"
        with open(output_file, "a", encoding="utf-8") as f:
            f.write(f"{diagnostic_log}\n")
