#!/bin/bash
# setup_canonical_repo.sh
# Automates the absolute structural refactoring of kryptic-agent

set -e

echo "[+] Starting canonical repository refactoring..."

# 1. Ensure dedicated project tracking directories exist
echo "[+] Creating runtime and data directories..."
mkdir -p data runtime src/core tests .github/workflows

# 2. Write setup.py package boundary
echo "[+] Generating setup.py..."
cat << 'EOF' > setup.py
from setuptools import setup, find_packages

setup(
    name="kryptic_agent",
    version="1.0.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "cryptography",
    ],
    python_requires=">=3.8",
)
EOF

# 3. Write pytest.ini mapping definition
echo "[+] Generating pytest.ini..."
cat << 'EOF' > pytest.ini
[pytest]
testpaths = tests
pythonpath = src
addopts = --strict-markers -v
EOF

# 4. Write pure .gitignore layout
echo "[+] Generating .gitignore..."
cat << 'EOF' > .gitignore
# Python Environment
__pycache__/
*.pyc
*.pyo
*.pyd
.pytest_cache/
*.egg-info/
dist/
build/

# Application Runtime Output
data/
runtime/
*.db
*.so
matrix_accelerator

# System and IDE
.DS_Store
.env
EOF

# 5. Write the monolithic consolidated workflow file
echo "[+] Generating .github/workflows/ci.yml..."
cat << 'EOF' > .github/workflows/ci.yml
name: Canonical CI Pipeline

on:
  push:
    branches: [ main, dev-hardware-integration, commercial ]
  pull_request:
    branches: [ main ]

jobs:
  validate-and-build:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout Source Code
      uses: actions/checkout@v4

    - name: Set up Python Environment
      uses: actions/setup-python@v5
      with:
        python-version: '3.10'
        cache: 'pip'

    - name: Install Runtime and Compiler Toolchains
      run: |
        sudo apt-get update
        sudo apt-get install -y g++ sqlite3 libsqlite3-dev

    - name: Install Dependencies
      run: |
        python -m pip install --upgrade pip
        pip install pytest cryptography
        pip install -e .

    - name: Compile Native Hardware Accelerator Layer
      run: |
        mkdir -p runtime
        g++ -O3 -shared -std=c++17 -fPIC \
          -I${{ github.workspace }}/src/core \
          ${{ github.workspace }}/src/core/kryptic_hardware_accelerator.cpp \
          -o ${{ github.workspace }}/runtime/libkryptic_accel.so

    - name: Run Test Suite Via Canonical Boundary
      run: |
        pytest
EOF

# 6. Write src/core/__init__.py package node
touch src/core/__init__.py

# 7. Write the hardened and import-safe core engine
echo "[+] Generating src/core/kryptic_agent_core.py..."
cat << 'EOF' > src/core/kryptic_agent_core.py
import os
import sys
import base64
import sqlite3
from pathlib import Path
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Dynamic Safe Evaluation of Project Base Directories
_FILE_PATH = Path(__file__).resolve()
PROJECT_ROOT = _FILE_PATH.parents[2]

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
        # Initialize parent node structures safely matching state context
        if HAS_ROS2:
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
        try:
            with sqlite3.connect(str(self.db_path)) as conn:
                cursor = conn.execute(
                    "SELECT nonce, payload FROM secure_state WHERE layer_id = ?",
                    (layer_id,)
                )
                row = cursor.fetchone()
                if not row:
                    return b""
                
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
EOF

# 8. Write tests/__init__.py package node
touch tests/__init__.py

# 9. Write canonical test suite validation suite
echo "[+] Generating tests/test_core.py..."
cat << 'EOF' > tests/test_core.py
import pytest
from core.kryptic_agent_core import KrypticAgentCore, HAS_ROS2

def test_agent_initialization_without_crashing():
    """Validates core stability, ensuring it isolates missing environmental layers smoothly."""
    agent = KrypticAgentCore(db_name="test_temp_memory.db")
    assert agent.db_path.name == "test_temp_memory.db"
    assert agent.db_path.exists() is True

def test_secure_weights_migration_workflow():
    """Validates end-to-end payload preservation under cryptography cycles."""
    agent = KrypticAgentCore(db_name="test_crypto_memory.db")
    mock_data = b"secure_layer_weights_matrix_v1"
    
    agent.persist_encrypted_payload("layer_0", mock_data)
    recovered_data = agent.read_encrypted_payload("layer_0")
    
    assert recovered_data == mock_data

def test_ros2_conditional_status():
    """Confirms modular architecture design posture across execution profiles."""
    if not HAS_ROS2:
        agent = KrypticAgentCore()
        assert "mock" in agent.name
EOF

# 10. Scrub structural duplicate test paths, root pollutions, and redundant configurations
echo "[+] Scrubbing legacy configuration noise, broken db files, and duplicate test tracks..."
rm -rf src/tests/ src/core/tests/ local_test_copies/
rm -f *.db app_telemetry.log agent_telemetry.log test_temp_memory.db test_crypto_memory.db
find .github/workflows/ -type f ! -name 'ci.yml' -delete

echo "[+] Execution completed flawlessly. Repository conforms to strict canonical rules."
