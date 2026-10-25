#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e

# Configuration Variables
CONTAINER_NAME="running-kryptic-node"
IMAGE_NAME="kryptic-agent-edge:latest"
HOST_PORT=8000
CONTAINER_PORT=8000
DATA_DIR="$(pwd)/data"

echo "=== Initializing Kryptic Node Deployment Script ==="

# 1. Ensure local data persistence path exists
if [ ! -d "$DATA_DIR" ]; then
    echo "[+] Creating persistent ledger directory at: $DATA_DIR"
    mkdir -p "$DATA_DIR"
fi

# 2. Check for and clean up existing containers with the same name
if [ "$(docker ps -aq -f name=^${CONTAINER_NAME}$)" ]; then
    echo "[!] Existing container found. Cleaning up environment..."
    
    if [ "$(docker ps -q -f name=^${CONTAINER_NAME}$)" ]; then
        echo "[-] Stopping active container: $CONTAINER_NAME"
        docker stop "$CONTAINER_NAME" > /dev/null
    fi
    
    echo "[-] Removing old container instance..."
    docker rm "$CONTAINER_NAME" > /dev/null
fi

# 3. Spin up the new runtime instance
echo "[+] Launching edge node tracking service..."
docker run -d \
    -p "${HOST_PORT}:${CONTAINER_PORT}" \
    -v "${DATA_DIR}:/app/data" \
    --name "$CONTAINER_NAME" \
    --restart unless-stopped \
    "$IMAGE_NAME"

# 4. Verify deployment state
echo "[+] Deployment successful!"
echo "------------------------------------------------"
echo "Container Name : $CONTAINER_NAME"
echo "Host Endpoint  : http://localhost:$HOST_PORT"
echo "Persistence    : $DATA_DIR -> /app/data"
echo "------------------------------------------------"
echo "[*] To view initialization telemetry, run: docker logs -f $CONTAINER_NAME"
