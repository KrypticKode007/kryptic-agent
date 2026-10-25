#!/usr/bin/env python3
"""
Kryptic-Agent Multi-Node Dynamic Cluster Process Launcher
Orchestrates parallel deployment routines across cluster boundaries concurrently.
"""

import sys
import time
import subprocess
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(message)s')
logger = logging.getLogger("KrypticLauncher")

def launch_cluster_nodes():
    nodes = {
        "8000": "node-01-ground-master [Active Inference Orchestrator]",
        "8001": "node-02-edge-tracking-alpha [Kalman Covariance Isolator]",
        "8002": "node-03-edge-tracking-beta [Kinematic Failsafe Mediator]"
    }
    
    processes = []
    logger.info("Initializing multi-node execution framework configuration...")

    try:
        for port, description in nodes.items():
            logger.info(f"Kicking off target cluster loop process on Port {port}: {description}")
            # Spawning concurrent isolated background tracking interfaces
            proc = subprocess.Popen(
                [sys.executable, "-m", "uvicorn", "src.api.telemetry_dashboard:app", "--port", port, "--log-level", "warning"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            processes.append((proc, description))
            time.sleep(0.2) # Avoid socket binding race condition frames

        logger.info("All distributed cluster tracking sub-nodes running. Press Ctrl+C to terminate the grid.")
        while True:
            time.sleep(1.0)

    except KeyboardInterrupt:
        logger.warning("Shutdown command intercepted by network orchestrator. Safeguarding node states...")
    finally:
        for proc, description in processes:
            logger.info(f"Decommissioning background daemon instance: {description}")
            proc.terminate()
            proc.wait()
        logger.info("Multi-agent cluster framework safely dismantled.")

if __name__ == "__main__":
    launch_cluster_nodes()
  
