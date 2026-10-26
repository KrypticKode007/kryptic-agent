#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

if [[ ! -d .venv ]]; then
  python3 -m venv .venv
fi
source .venv/bin/activate

export CYCLONE_DDS_URI="$ROOT_DIR/cyclone_dds_config.xml"
python main.py
