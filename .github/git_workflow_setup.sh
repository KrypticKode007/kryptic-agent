#!/bin/bash
# ==============================================================================
# KRYPTIC AGENT MASTER GIT WORKFLOW SETUP SCRIPT
# Automatically provisions OpenKey SSH architecture and deploys branch layouts.
# Owner: Brandon Mark Wilson (KrypticKode007)
# Repo Target: kryptic-agent
# System Epoch: October 2026
# ==============================================================================

# Halt script operations instantly if any individual sub-command fails
set -e

# Identity and routing variables
GH_USER="KrypticKode007"
GH_EMAIL="b.wilson@students.maestrocollege.edu"
GH_REPO="kryptic-agent"
WORKSPACE_DIR="$HOME/termux-sentience-core"

echo "=================================================================="
echo "⚡ INITIALIZING MASTER GIT WORKFLOW INFRASTRUCTURE FOR KRYPTIC ⚡"
echo "=================================================================="

# Step 1: Initialize local directory environment workspace
if [ ! -d "$WORKSPACE_DIR" ]; then
    echo "📁 Creating active project workspace path..."
    mkdir -p "$WORKSPACE_DIR"
fi
cd "$WORKSPACE_DIR"

# Step 2: Provision local Git folder and identity metadata parameters
echo "⚙️ Establishing local Git repository footprint structures..."
git init

git config user.name "$GH_USER"
git config user.email "$GH_EMAIL"

# Step 3: Generate the Asymmetric Cryptographic Keys in OpenKey/PEM Format
echo "🔐 Generating 4096-bit RSA deployment keys in OpenKey PEM format..."
mkdir -p ~/.ssh
chmod 700 ~/.ssh

# Overwrite any existing key safely with traditional open key PEM headers
ssh-keygen -t rsa -b 4096 -m PEM -C "$GH_EMAIL" -f ~/.ssh/kryptic_deploy_key -N ""

chmod 600 ~/.ssh/kryptic_deploy_key
chmod 644 ~/.ssh/kryptic_deploy_key.pub

# Step 4: Map local SSH routing configurations
echo "🛠️ Configuring background SSH client profile routes..."
SSH_CONFIG_FILE="$HOME/.ssh/config"

cat << EOF > "$SSH_CONFIG_FILE"
# Dedicated secure key routing path signature for Kryptic Agent repo
Host github-kryptic
    HostName github.com
    User git
    IdentityFile ~/.ssh/kryptic_deploy_key
    IdentitiesOnly yes
EOF

chmod 600 "$SSH_CONFIG_FILE"

# Step 5: Link local project directory to the OpenKey upstream remote alias URL
echo "🔄 Connecting local remote tracking paths to secure SSH host address..."
if git remote | grep -q "^origin$"; then
    git remote set-url origin "git@github-kryptic:${GH_USER}/${GH_REPO}.git"
else
    git remote add origin "git@github-kryptic:${GH_USER}/${GH_REPO}.git"
fi

# Step 6: Create and baseline the required multi-branch architecture framework
echo "🌿 Structuring multi-branch development lifecycle paths..."

# Create placeholder trackers so Git allows empty branch allocations to materialize
echo "# Kryptic Core Production Trunk" > README.md
git add README.md
git commit -m "Initial baseline commit for production trunk allocation."

# Standardize primary execution branch name to main
git branch -M main

# Generate the companion branches sequentially
git branch development
git branch feature/vocal-cloning-pipeline
git branch feature/internet-knowledge-fetcher
git branch telemetry/hardware-longevity
git branch archive/theoretical-generations

echo "=================================================================="
echo "✅ [SUCCESS] ALL ENVIRONMENT CORE ASSETS SUCCESSFULLY DEPLOYED"
echo "=================================================================="
echo "📋 YOUR ACTION REQUIRED: Copy the OpenKey public text block below,"
echo "   add it to your GitHub Deploy Keys under '$GH_USER/$GH_REPO',"
echo "   and make sure to check the 'Allow write access' box!"
echo "=================================================================="
echo ""
cat ~/.ssh/kryptic_deploy_key.pub
echo ""
echo "=================================================================="
echo "👉 After pasting the key to GitHub, verify your link via: 'ssh -T git@github-kryptic'"
