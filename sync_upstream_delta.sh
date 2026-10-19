#!/usr/bin/env bash
# sync_upstream_delta.sh
# Safely pulls down recent validation modifications from the remote main branch 
# without leaving orphaned merge commits or tracking discrepancies.

set -euo pipefail

REMOTE_NAME="origin"
PRIMARY_BRANCH="main"

echo "======================================================================"
echo "🔄 RUNNING INTERACTIVE LIVE REPOSITORY REBASE & SYNC SERVICE"
echo "======================================================================"

# 1. Check if the directory is a valid git repository
if [ ! -d .git ]; then
    echo "❌ Error: System terminal context is not pointing to a valid Git repository root."
    exit 1
fi

# 2. Preserve uncommitted local telemetry hacks using git stash layers
if ! git diff-index --quiet HEAD --; then
    echo "[*] Local uncommitted modifications detected inside tracking directory."
    echo "    -> Stash preservation protocol initiated..."
    git stash save "kryptic_local_drift_backup_$(date +%s)"
fi

# 3. Pull fresh change tracking arrays from the GitHub remote origin
echo "[*] Fetching delta updates from remote origin: ${REMOTE_NAME}..."
git fetch "$REMOTE_NAME" --prune --tags

# 4. Execute a fast-forward rebase to apply latest remote test patches cleanly
echo "[*] Rebasing active local workspace branch onto latest ${REMOTE_NAME}/${PRIMARY_BRANCH}..."
if git rebase "${REMOTE_NAME}/${PRIMARY_BRANCH}"; then
    echo "✅ Success: Local tracking loops are fully synchronized with remote commits."
else
    echo "⚠️  Alert: Conflict detected during rebase operation."
    echo "    Please resolve merge conflicts manually, then run 'git rebase --continue'."
    exit 2
fi

# 5. Restore uncommitted local hacks if they were stashed away earlier
if git stash list | grep -q "kryptic_local_drift_backup"; then
    echo "[*] Restoring stashed workspace changes onto fresh synchronized base..."
    git stash pop
fi

echo "======================================================================"
echo "⚡ WORKSPACE TRACKING SYNCHRONIZED TO REMOTE CONVENTIONS"
echo "======================================================================"
