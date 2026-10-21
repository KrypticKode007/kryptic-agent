#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# ==========================================
# 1. CORE REPOSITORY CONFIGURATION
# ==========================================
REPO_OWNER="KrypticKode007"
REPO_NAME="kryptic-agent"
REMOTE_URL="https://github.com{REPO_OWNER}/${REPO_NAME}.git"

echo "========================================================="
echo "Starting Configuration Setup for: ${REPO_OWNER}/${REPO_NAME}"
echo "========================================================="

# ==========================================
# 2. LOCAL ENVIRONMENT INITIALIZATION
# ==========================================
# Check if current directory is already a git repo, if not, clone or init
if [ ! -d ".git" ]; then
    echo "⚙️ Initializing local Git repository..."
    if git clone "$REMOTE_URL"; then
        cd "$REPO_NAME"
    else
        echo "Could not clone directly. Setting up an empty folder and pulling..."
        mkdir -p "$REPO_NAME" && cd "$REPO_NAME"
        git init
        git remote add origin "$REMOTE_URL"
    fi
else
    echo "✅ Found existing Git repository framework."
    # Ensure origin is pointed correctly
    git remote set-url origin "$REMOTE_URL" 2>/dev/null || git remote add origin "$REMOTE_URL"
fi

# ==========================================
# 3. GLOBAL & LOCAL GIT PERFORMANCE FLAGS
# ==========================================
echo "⚙️ Configuring tracking, pruning, and merge preferences..."
git config --local push.autoSetupRemote true
git config --local fetch.prune true
git config --local pull.rebase false  # Prefers standard fast-forward merges

# ==========================================
# 4. CONFIGURE & FETCH ALL REMOTES/BRANCHES
# ==========================================
echo "⚙️ Forcing remote refspec to track ALL branches..."
# This ensures that git fetch explicitly grabs every single remote branch 
git config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"

echo "⚙️ Fetching latest snapshots from GitHub..."
git fetch origin

# Get the default branch name dynamically (usually main or master)
DEFAULT_BRANCH=$(git remote show origin | grep "HEAD branch" | sed 's/.*: //')
echo "🔹 Detected Default Branch: $DEFAULT_BRANCH"

# ==========================================
# 5. AUTOMATED BRANCH TRACKING LOOP
# ==========================================
echo "⚙️ Setting up tracking configurations for all individual branches..."

# Loop through all remote branches and link them locally
for remote_branch in $(git branch -r | grep -v '\->'); do
    # Extract the clean branch name without the "origin/" prefix
    local_branch=$(echo "$remote_branch" | sed 's/origin\///' | xargs)
    
    if [ "$local_branch" == "$DEFAULT_BRANCH" ]; then
        # Ensure default branch is checked out and tracked properly
        git checkout -B "$DEFAULT_BRANCH" "origin/$DEFAULT_BRANCH"
    else
        echo "   -> Tracking branch: $local_branch"
        # Create local branch if it doesn't exist, and force track remote
        git branch --track "$local_branch" "$remote_branch" 2>/dev/null || true
    fi
done

# Return to default branch
git checkout "$DEFAULT_BRANCH"
echo "⚙️ Pulling everything down to finalize synchronization..."
git pull --all

echo "========================================================="
echo " 🎉 Configuration Complete! All remote branches are synced."
echo "========================================================="
