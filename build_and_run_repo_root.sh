#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

if [[ ! -d .venv ]]; then
  python3 -m venv .venv
fi

source .venv/bin/activate
python -m pip install --upgrade pip >/dev/null
python -m pip install -r requirements.txt
python -m compileall .
pytest tests -q
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --parallel
export CYCLONE_DDS_URI="$ROOT_DIR/cyclone_dds_config.xml"
python main.py
