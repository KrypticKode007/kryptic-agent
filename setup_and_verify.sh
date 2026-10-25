#!/usr/bin/env bash
# ==============================================================================
# Kryptic-Agent Production Environment Setup & Verification Pipeline
# This script automates dependency installation, compilation, binary verification,
# and project testing to ensure real hardware execution compliance.
# ==============================================================================

set -e # Exit immediately if a command exits with a non-zero status

echo "==== [1/4] Installing System & Python Dependencies ===="
# Upgrade pip and install repository requirements
python3 -m pip install --upgrade pip
if [ -f requirements.txt ]; then
    python3 -m pip install -r requirements.txt
else
    echo "[INFO] requirements.txt not found, skipping python package installation."
fi

# Update package lists and install native build tools
sudo apt-get update
sudo apt-get install -y g++ cmake sqlite3 libsqlite3-dev

echo "==== [2/4] Compiling Bare-Metal C++ Hardware Accelerator ===="
# Ensure the source directory layout matches the production specification
mkdir -p src

# Compile the target C++ optimization bridge with production flags
g++ -O3 -std=c++17 -Wall -Wextra -Werror src/kryptic_hardware_accelerator.cpp -o matrix_accelerator
chmod +x matrix_accelerator

echo "==== [3/4] Verifying Matrix Accelerator Binary Run ===="
# Execute with the specified test parameters
./matrix_accelerator 0.75 0.20

echo "==== [4/4] Executing Project Regression Testing Matrix ===="
# Run the automated pytest pipeline if the testing directory is populated
if [ -d tests ]; then
    pytest tests -v
else
    echo "[INFO] tests directory not found, skipping pytest suite."
fi

echo "[SUCCESS] Kryptic-Agent execution setup pipeline completed."
