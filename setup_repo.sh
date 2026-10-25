#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e

# Configuration
REPO_URL="https://github.com/kryptickode007/kryptickode007-holonomic-sentience-core.git"
CONTAINER_NAME="running-kryptic-node"
IMAGE_NAME="kryptic-agent-edge:latest"
HOST_PORT=8000
CONTAINER_PORT=8000
DATA_DIR="$(pwd)/data"

echo "=== Initializing Kryptic Edge Repository Setup Utility ==="

# 1. Check for local Git context or clone the core architecture layout
if [ ! -d ".git" ]; then
    echo "[+] Root repository context missing. Pulling framework deployment tree..."
    git clone "$REPO_URL" temp_repo_clone
    mv temp_repo_clone/* temp_repo_clone/.* . 2>/dev/null || true
    rm -rf temp_repo_clone
else
    echo "[+] Verified valid working tree context locally."
fi

# 2. Ensure data infrastructure layers exist
if [ ! -d "$DATA_DIR" ]; then
    echo "[+] Mapping isolation zone data volume storage path at: $DATA_DIR"
    mkdir -p "$DATA_DIR"
fi

# 3. Compile the local edge node image from the project context Dockerfile
if [ -f "Dockerfile" ]; then
    echo "[+] Dockerfile located. Building container image asset: $IMAGE_NAME..."
    docker build -t "$IMAGE_NAME" .
else
    echo "[!] Warning: Native Dockerfile missing in current path. Attempting image allocation check..."
    if ! docker images --format '{{.Repository}}:{{.Tag}}' | grep -Eq "^${IMAGE_NAME}$"; then
        echo "[!] Error: Targeted image resource context not found locally."
        exit 1
    fi
fi

# 4. Clean up any stale instances operating on the system boundaries
if [ "$(docker ps -aq -f name=^${CONTAINER_NAME}$)" ]; then
    echo "[!] Active collision detected with instance name: $CONTAINER_NAME. Cleaning context..."
    if [ "$(docker ps -q -f name=^${CONTAINER_NAME}$)" ]; then
        docker stop "$CONTAINER_NAME" > /dev/null
    fi
    docker rm "$CONTAINER_NAME" > /dev/null
fi

# 5. Spin up the detached daemon with isolation volumes mapped
echo "[+] Launching edge node container daemon..."
docker run -d \
    -p "${HOST_PORT}:${CONTAINER_PORT}" \
    -v "${DATA_DIR}:/app/data" \
    --name "$CONTAINER_NAME" \
    --restart unless-stopped \
    "$IMAGE_NAME"

echo "[+] Node deployment complete!"
echo "---------------------------------------------------------"
echo "[*] Handing control sequence over to the diagnostic monitoring engine..."
echo "---------------------------------------------------------"
sleep 2

# 6. Execute the telemetry watchdog interface if present
if [ -f "./monitor_edge_node.sh" ]; then
    chmod +x ./monitor_edge_node.sh
    exec ./monitor_edge_node.sh
else
    echo "[!] monitor_edge_node.sh not found in this folder path."
    echo "[*] Use: 'docker logs -f $CONTAINER_NAME' to manually review output parameters."
fi
