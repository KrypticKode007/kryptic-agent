#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

echo "[1/6] Creating virtual environment..."
if [[ ! -d .venv ]]; then
  python3 -m venv .venv
fi
source .venv/bin/activate

echo "[2/6] Upgrading pip..."
python -m pip install --upgrade pip >/dev/null

echo "[3/6] Installing Python dependencies..."
python -m pip install -r requirements.txt

echo "[4/6] Running Python syntax validation..."
python -m compileall .

echo "[5/6] Running Python tests..."
pytest tests -q

echo "[6/6] Configuring and building C++ targets..."
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --parallel

echo "Build pipeline completed successfully."
