#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e

# Configuration
CONTAINER_NAME="running-kryptic-node"

# Operational Threshold Limits
MAX_CPU_THRESHOLD=85       # Maximum allowable CPU usage percentage
MAX_MEM_THRESHOLD=90       # Maximum allowable Memory usage percentage
CHECK_INTERVAL_SECS=5      # Frequency of automated evaluation sweeps

echo "=== Kryptic Node Protected Diagnostic & Telemetry Watchdog ==="

# 1. Verify container existence and state
if ! docker ps -a --format '{{.Names}}' | grep -Eq "^${CONTAINER_NAME}$"; then
    echo "[!] Error: Container '${CONTAINER_NAME}' does not exist."
    echo "[*] Run your deployment script first to initialize the container."
    exit 1
fi

# Fallback sequence handler to safely cycle a degrading container instance
reboot_container_node() {
    local reason="$1"
    echo -e "\n[!!!] CRITICAL RESOURCE EXCEEDED: $reason"
    echo "[!] Initiating automated corrective recovery protocol..."
    echo "[-] Power cycling container: $CONTAINER_NAME"
    docker restart "$CONTAINER_NAME" > /dev/null
    echo "[+] Recovery cycle complete. Node state refreshed successfully."
    echo "---------------------------------------------------------"
}

# 2. Main operational loop monitoring system resource boundaries
echo "[+] Watchdog active. Evaluating metrics every ${CHECK_INTERVAL_SECS}s..."
echo "[*] Monitoring Limits -> CPU Max: ${MAX_CPU_THRESHOLD}% | MEM Max: ${MAX_MEM_THRESHOLD}%"
echo "[*] Press [CTRL+C] to terminate the monitoring engine and drop to log stream."
echo "---------------------------------------------------------"

# Capture SIGINT (Ctrl+C) to terminate the resource loop and drop straight to live application logs
trap 'echo -e "\n\n[-] Watchdog monitoring suspended by user. Transferring to application logs...\n"; break' SIGINT

while true; do
    # Fetch container state; check if it is running before inspecting utilization metrics
    STATUS=$(docker inspect -f '{{.State.Running}}' "$CONTAINER_NAME" 2>/dev/null || echo "false")
    if [ "$STATUS" != "true" ]; then
        echo "[!] Warning: Container is not in a running state. Attempting auto-start..."
        docker start "$CONTAINER_NAME" > /dev/null && sleep 2
        continue
    fi

    # Extract raw metrics from docker stats engine
    STATS_RAW=$(docker stats --no-stream --format "{{.CPUPerc}},{{.MemPerc}}" "$CONTAINER_NAME" 2>/dev/null || echo "0.00%,0.00%")
    
    # Parse out percentages and strip formatting signs for numeric checking
    CPU_RAW=$(echo "$STATS_RAW" | cut -d',' -f1 | tr -d '%[:space:]')
    MEM_RAW=$(echo "$STATS_RAW" | cut -d',' -f2 | tr -d '%[:space:]')

    # Convert floating point values into integers for baseline shell evaluation comparisons
    CPU_VAL=$(printf "%.0f" "$CPU_RAW" 2>/dev/null || echo 0)
    MEM_VAL=$(printf "%.0f" "$MEM_RAW" 2>/dev/null || echo 0)

    echo "[Telemetry Check] CPU: ${CPU_VAL}% / ${MAX_CPU_THRESHOLD}% | MEM: ${MEM_VAL}% / ${MAX_MEM_THRESHOLD}%"

    # Evaluate performance data against configured limits
    if [ "$CPU_VAL" -gt "$MAX_CPU_THRESHOLD" ]; then
        reboot_container_node "CPU utilization spike at ${CPU_VAL}%"
        sleep 5
    elif [ "$MEM_VAL" -gt "$MAX_MEM_THRESHOLD" ]; then
        reboot_container_node "Memory threshold leakage at ${MEM_VAL}%"
        sleep 5
    fi

    sleep "$CHECK_INTERVAL_SECS"
done

# Reset trap structure for consecutive streaming standard out tasks
trap - SIGINT

# 3. Stream initialization and tracking logs (docker logs)
echo "---------------------------------------------------------"
echo "[+] Fetching Active Holonomic Sentience Core Logs..."
echo "[*] Streaming runtime output below. Press [CTRL+C] to close the sequence."
echo "---------------------------------------------------------"

docker logs -f "$CONTAINER_NAME"
