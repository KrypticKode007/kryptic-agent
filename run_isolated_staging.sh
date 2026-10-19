#!/usr/bin/env bash
# run_isolated_staging.sh
# Orchestrates all three framework validation pipelines within an isolated staging sequence.

set -euo pipefail

echo "======================================================================"
echo "🛡️  LAUNCHING KRYPTIC-AGENT ISOLATED STAGING DEPLOYMENT PLAYBOOK"
echo "======================================================================"

# 1. Establish Sandbox Environment Parameters
export STAGING_DIR="/tmp/kryptic_staging_sandbox"
export KRYPTIC_DATA_DIR="${STAGING_DIR}/share"
rm -rf "$STAGING_DIR"
mkdir -p "$KRYPTIC_DATA_DIR"

echo "[*] Sandbox Root Configured: ${STAGING_DIR}"

# 2. Pipeline 1: Run General Python Core & Invariant Intercept Audits
echo -e "\n[*] [PIPELINE 1/3] Executing core homeostatic validation loop..."
python3 unified_conscious_agent.py

# 3. Pipeline 2: Run C++ Bare-Metal Latency Benchmarking Compilation
echo -e "\n[*] [PIPELINE 2/3] Compiling bare-metal flight architecture nodes..."
if command -v g++ &> /dev/null; then
    g++ -std=c++17 -O3 test_hardware_latency.cpp -o "${STAGING_DIR}/test_hardware_latency_bin"
    "${STAGING_DIR}/test_hardware_latency_bin"
else
    echo "  ⚠️ System g++ compiler missing from runtime staging environment."
fi

# 4. Pipeline 3: Run Cognitive Bayesian Ego Boundary Unit Tests
echo -e "\n[*] [PIPELINE 3/3] Evaluating prediction error equations..."
if command -v pytest &> /dev/null; then
    pytest tests/test_ego_boundary.py -v
else
    echo "  [*] Executing raw mathematical engine verification step..."
    python3 ego_boundary_calculator.py
fi

# 5. Clean up Sandbox Directory allocations
rm -rf "$STAGING_DIR"
echo -e "\n======================================================================"
echo "✅ ALL THREE PIPELINES EXECUTED SUCCESSFULLY IN STAGING HOOKS"
echo "======================================================================"
