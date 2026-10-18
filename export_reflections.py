#!/usr/bin/env python3
"""
export_reflections.py
Custom history export utility for the kryptic-agent repository.
Extracts transactional agent reflections and memory snapshots across operations,
packaging them into clean portable formats before major branch merges.
"""

import os
import sys
import json
import sqlite3
import csv
from datetime import datetime

def export_agent_history():
    """Extracts local database reflections and handles migration backups safely."""
    # Resolve system path directly from environment parameters
    xdg_data = os.environ.get("KRYPTIC_DATA_DIR", os.path.expanduser("~/.local/share/kryptic-agent"))
    db_path = os.path.join(xdg_data, "kryptic_history.db")
    
    # Fallback checking for local workspace testing
    if not os.path.exists(db_path):
        db_path = "kryptic_history.db"
        if not os.path.exists(db_path):
            print(f"❌ Error: Active history ledger database not found at {db_path}.")
            sys.exit(1)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    export_filename = f"kryptic_reflections_backup_{timestamp}.csv"

    print(f"[*] Accessing core history tables from: {db_path}")
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM runtime_logs ORDER BY epoch_id ASC")
            records = cursor.fetchall()
            
            if not records:
                print("⚠️  Warning: Target relational ledger is empty. No tracking logs found.")
                return

            # Securely stream database blocks directly out to standard CSV ledger tables
            with open(export_filename, mode="w", newline="", encoding="utf-8") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(["Epoch ID", "Timestamp", "Internal Monologue", "Stamina Value", "Hardware Telemetry Snapshot"])
                
                for row in records:
                    writer.writerow(row)
                    
        print(f"✅ Success: {len(records)} autobiographical reflection records exported to: {export_filename}")
    except Exception as err:
        print(f"❌ Critical Migration Failure: {str(err)}")
        sys.exit(1)

if __name__ == "__main__":
    export_agent_history()
