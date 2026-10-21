#!/usr/bin/env bash
set -euo pipefail

echo "===================================================================="
echo "🔀 INITIALIZING AUTOMATED GIT BRANCH DESYNCHRONIZER"
echo "===================================================================="

# Verify git repository initialization
if [ ! -d .git ]; then
    echo "[❌ ERROR] Current directory is not a valid git repository context."
    exit 1
fi

# Store the current branch name to return to later
ORIGINAL_BRANCH=$(git branch --show-current)
echo "[🔗] Stashing current working state baseline on branch: ${ORIGINAL_BRANCH}"

# 1. Update Hardware Integration Branch
echo -e "\n[🛰️] Syncing Hardware Integration Architecture..."
git checkout dev-hardware-integration 2>/dev/null || git checkout -b dev-hardware-integration

# Ensure directory files are accurately added
git add src/hardware_integration/CMakeLists.txt tools/verification/verify_hardware_runtime_poc.py

if ! git diff-index --quiet HEAD --; then
    git commit -m "feat(hardware): implement native POSIX clocks, -O3 compiler optimization targets, and low-latency validation telemetry sandbox"
    echo "[⬆️] Pushing updates to origin/dev-hardware-integration..."
    git push origin dev-hardware-integration
else
    echo "[⚠️] No unique structural deltas found for dev-hardware-integration branch."
fi

# 2. Update Commercial / Deployment Suite Branch
echo -e "\n[💼] Syncing Commercial Infrastructure Pipeline..."
git checkout commercial 2>/dev/null || git checkout -b commercial

# Ensure launch config architecture files are added
git add config/launch/kryptic_edge_launch.py

if ! git diff-index --quiet HEAD --; then
    git commit -m "feat(commercial): integrate high-priority ROS 2 real-time priority kernel launch configurations"
    echo "[⬆️] Pushing updates to origin/commercial..."
    git push origin commercial
else
    echo "[⚠️] No unique structural deltas found for commercial branch."
fi

# 3. Return to initial branch workspace
echo -e "\n[🔄] Reverting workspace view back to baseline branch: ${ORIGINAL_BRANCH}"
git checkout "${ORIGINAL_BRANCH}"

echo "===================================================================="
echo "🎯 REPOSITORY SYNC COMPLETED SUCCESSFULLY"
echo "===================================================================="
