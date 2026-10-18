#!/usr/bin/env bash
# setup_env.sh
# Automated local installation playbook for setting up environment variables,
# configuring directory paths, and establishing the local SQLite history folder.

set -euo pipefail

# 1. Define standard cybernetic workspace layout directory structures
echo "======================================================================"
echo "⚙️  KRYPTIC-AGENT PLAYBOOK: CONFIGURING LOCAL ENVIRONMENT PATHS"
echo "======================================================================"

# Adheres to clean system specifier configurations
XDG_DATA_HOME="${XDG_DATA_HOME:-$HOME/.local/share}"
KRYPTIC_DATA_DIR="$XDG_DATA_HOME/kryptic-agent"
DB_NAME="kryptic_history.db"

echo "[*] Establishing system tracking paths..."
echo "    System Data Path: $KRYPTIC_DATA_DIR"

# Create persistence layers safely
mkdir -p "$KRYPTIC_DATA_DIR"
mkdir -p "tests"
mkdir -p ".github/workflows"

# 2. Injecting system level parameters into profile structures
PROFILE_FILE=""
if [[ -f "$HOME/.bashrc" ]]; then
    PROFILE_FILE="$HOME/.bashrc"
elif [[ -f "$HOME/.zshrc" ]]; then
    PROFILE_FILE="$HOME/.zshrc"
fi

if [[ -n "$PROFILE_FILE" ]]; then
    echo "[*] Injecting environment variable paths into $PROFILE_FILE..."
    if ! grep -q "KRYPTIC_DATA_DIR" "$PROFILE_FILE"; then
        echo -e "\n# Kryptic Agent Environment Variables" >> "$PROFILE_FILE"
        echo "export KRYPTIC_DATA_DIR=\"$KRYPTIC_DATA_DIR\"" >> "$PROFILE_FILE"
        echo "✅ Environment variables written out to target user profiles."
    else
        echo "    Environment keys already mapped inside profile registry."
    fi
fi

# 3. Initializing persistent transactional SQLite storage files
echo "[*] Creating persistent transactional SQLite ledger tracking databases..."
python3 -c "
import os, sqlite3
db_path = os.path.join('$KRYPTIC_DATA_DIR', '$DB_NAME')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS runtime_logs (
        epoch_id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp REAL,
        internal_monologue TEXT,
        stamina_marker REAL,
        telemetry_snapshot TEXT
    )
''')
conn.commit()
conn.close()
print('✅ SQLite History Folder initialized at: ' + db_path)
"

echo "[*] Executing local dependencies checks..."
if command -v pip3 &> /dev/null; then
    pip3 install -q ruff black pytest || echo "⚠️ Non-critical: Could not install local dev packages."
fi

echo "======================================================================"
echo "⚡ INSTALLATION PLAYBOOK COMPLETE: RUN 'source $PROFILE_FILE' TO FINALISE"
echo "======================================================================"
