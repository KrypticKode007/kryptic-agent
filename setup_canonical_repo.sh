#!/bin/bash
set -e

echo "[+] Canonicalizing repo layout..."

mkdir -p data runtime src/core tests .github/workflows

cat > setup.py <<'EOF'
from setuptools import setup, find_packages

setup(
    name="kryptic_agent",
    version="1.0.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=True,
    install_requires=["cryptography"],
    python_requires=">=3.8",
)
EOF

cat > pytest.ini <<'EOF'
[pytest]
testpaths = tests
addopts = -v
EOF

cat > .gitignore <<'EOF'
__pycache__/
*.pyc
*.pyo
*.pyd
.pytest_cache/
*.egg-info/
build/
dist/
data/
runtime/
*.db
*.log
matrix_accelerator
.DS_Store
.env
EOF

cat > .github/workflows/ci.yml <<'EOF'
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
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.10"
          cache: "pip"

      - name: Install toolchain
        run: |
          sudo apt-get update
          sudo apt-get install -y g++ sqlite3 libsqlite3-dev

      - name: Install deps
        run: |
          python -m pip install --upgrade pip
          pip install pytest cryptography
          pip install -e .

      - name: Build native accelerator
        run: |
          mkdir -p runtime
          g++ -O3 -std=c++17 -Wall -Wextra -Werror \
            "${{ github.workspace }}/kryptic_hardware_accelerator.cpp" \
            -o "${{ github.workspace }}/runtime/matrix_accelerator"

      - name: Run tests
        run: pytest
EOF

touch src/core/__init__.py
touch tests/__init__.py

cat > tests/conftest.py <<'EOF'
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
EOF

cat > src/core/kryptic_agent_core.py <<'EOF'
import os
import sqlite3
import base64
import sys
from pathlib import Path
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
RUNTIME_DIR = PROJECT_ROOT / "runtime"
DATA_DIR.mkdir(parents=True, exist_ok=True)
RUNTIME_DIR.mkdir(parents=True, exist_ok=True)

try:
    import rclpy
    from rclpy.node import Node
    HAS_ROS2 = True
except ImportError:
    HAS_ROS2 = False
    class Node:
        def __init__(self, name):
            self.name = name

class KrypticAgentCore(Node):
    def __init__(self, db_name="kryptic_memory.db"):
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
        nonce = os.urandom(12)
        encrypted = self.aesgcm.encrypt(nonce, payload_bytes, None)
        b64_nonce = base64.b64encode(nonce).decode("utf-8")
        b64_payload = base64.b64encode(encrypted).decode("utf-8")

        with sqlite3.connect(str(self.db_path)) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO secure_state (layer_id, nonce, payload) VALUES (?, ?, ?)",
                (layer_id, b64_nonce, b64_payload),
            )
            conn.commit()

    def read_encrypted_payload(self, layer_id: str) -> bytes:
        with sqlite3.connect(str(self.db_path)) as conn:
            row = conn.execute(
                "SELECT nonce, payload FROM secure_state WHERE layer_id = ?",
                (layer_id,),
            ).fetchone()
            if not row:
                return b""
            nonce = base64.b64decode(row[0].encode("utf-8"))
            payload = base64.b64decode(row[1].encode("utf-8"))
            return self.aesgcm.decrypt(nonce, payload, None)

    def write_runtime_telemetry_dump(self, diagnostic_log: str):
        output_file = RUNTIME_DIR / "agent_telemetry.log"
        with open(output_file, "a", encoding="utf-8") as f:
            f.write(f"{diagnostic_log}\n")
EOF

cat > tests/test_core.py <<'EOF'
import pytest
from core.kryptic_agent_core import KrypticAgentCore, HAS_ROS2

def test_agent_initialization_without_crashing():
    agent = KrypticAgentCore(db_name="test_temp_memory.db")
    assert agent.db_path.name == "test_temp_memory.db"
    assert agent.db_path.exists() is True

def test_secure_weights_migration_workflow():
    agent = KrypticAgentCore(db_name="test_crypto_memory.db")
    payload = b"secure_layer_weights_matrix_v1"
    agent.persist_encrypted_payload("layer_0", payload)
    recovered = agent.read_encrypted_payload("layer_0")
    assert recovered == payload

def test_ros2_conditional_status():
    agent = KrypticAgentCore()
    if not HAS_ROS2:
        assert "mock" in agent.name
EOF

rm -f ./*.db ./*.log
rm -f ./test_ego_boundary.py
rm -rf ./tests/tests
rm -rf ./src/tests
rm -rf ./src/core/tests
rm -rf ./local_test_copies

find .github/workflows -type f ! -name 'ci.yml' -delete

echo "[+] Canonical repo setup complete."
