#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e

# Configuration
CONTAINER_NAME="running-kryptic-node"

echo "=== Kryptic Node Telemetry & Diagnostic Interface ==="

# 1. Verify container existence and state
if ! docker ps -a --format '{{.Names}}' | grep -Eq "^${CONTAINER_NAME}$"; then
    echo "[!] Error: Container '${CONTAINER_NAME}' does not exist."
    echo "[*] Run your deployment script first to initialize the container."
    exit 1
fi

CONTAINER_STATUS=$(docker inspect -f '{{.State.Status}}' "$CONTAINER_NAME")
echo "[+] Container Status: $CONTAINER_STATUS"

# 2. Open an active streaming window for container resource metrics (docker stats)
echo "---------------------------------------------------------"
echo "[+] Initializing Container Resource Monitoring..."
echo "[*] Displaying CPU, Memory, I/O, and Network utilization."
echo "[*] Press [CTRL+C] once to exit resource tracking and view system logs."
echo "---------------------------------------------------------"

# Capture SIGINT (Ctrl+C) during stats to break out and continue to the logs step smoothly
trap 'echo -e "\n\n[-] Exiting metrics view. Transferring to application logs...\n"; trap - SIGINT' SIGINT

# Execute stats once to show initial state, or continuously loop with a stream
docker stats --no-stream "$CONTAINER_NAME"
echo ""
echo "[*] Streaming live stats (Press Ctrl+C to drop to app log stream)..."
docker stats "$CONTAINER_NAME"

# Reset trap for safe execution downstream
trap - SIGINT

# 3. Stream initialization and tracking logs (docker logs)
echo "---------------------------------------------------------"
echo "[+] Fetching Active Holonomic Sentience Core Logs..."
echo "[*] Streaming runtime output below. Press [CTRL+C] to close the sequence."
echo "---------------------------------------------------------"

docker logs -f "$CONTAINER_NAME"
