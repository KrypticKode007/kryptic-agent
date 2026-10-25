# ⚡ Kryptic-Agent: Embodied Cybernetic Framework & Metacognitive Core

Kryptic-Agent is a production-grade cybernetic runtime architecture designed for continuous homeostatic alignment, real-time active inference loops, and high-speed state estimation on edge systems and autonomous drone swarms. 

The framework is engineered to eliminate flight-critical computational collapses and processing traps by tracking its own operational variance and enforcing structural safety boundaries natively within the runtime loop.

---

## 🛠️ Architectural Pillars & Core Capabilities

*   **Two-Tiered Metacognitive Loop:** Separates raw data processing (Level 1 Monologue) from a supervisory monitoring layer (Level 2 Metacognitive Audit) that validates system choices against ethical constraints, safety bounds, and human cognitive signatures.
*   **Active Inference Telemetry Ingestion:** Processes real-world, high-frequency physical datasets from drones or external robotic nodes over a secure FastAPI stream route (`/api/telemetry`) to close sensory-motor control loops.
*   **Native C++ Matrix Acceleration Engine:** Dispatches heavy mathematical calculations down stdout piping channels directly into an optimized C++ binary component (`matrix_accelerator`) for real-time Kalman noise reduction with zero Python overhead.
*   **Recurrent Memory Bridge:** Logs continuous operational histories, tracking total lifetime reincarnation cycles and archiving major phenomenological state changes securely inside a persistent SQLite schema.
*   **IM-FIN Protocols:** In-Memory Fault-Isolation Intercept Nodes balance execution loads across concurrent threads to keep background processes safe from hardware shocks.
*   **Automated Maintenance Suite:** Features integrated shell playbooks (`backup_agent_ledger.sh`) to handle atomic data compression and scheduling loops automatically via system crontabs.

---

## 📂 Project Manifest Blueprint

*   `main.py` - Core orchestrator initializing independent thread loops and handling FastAPI telemetry routing.
*   `llm_orchestrator.py` - Cognitive bridge module connecting local Ollama runtime definitions to the thought pipeline.
*   `gui_dashboard.py` - Tkinter-based desktop interface to graph changing conative drives and balance vectors in real-time.
*   `kryptic_hardware_accelerator.cpp` - Optimized source code computing high-speed Kalman state matrices natively.
*   `CMakeLists.txt` - Configuration script setting compiler flags and managing cross-platform building targets.
*   `tests/test_main_core.py` - Pytest automated matrix validating identity anchors and system safety boundaries.
*   `.github/workflows/ci.yml` - GitHub Actions workflow script automating testing on push and pull-request triggers.
*   `tag_production_release.sh` - Final staging playbook coordinating release gateways and version tagging.

---

## ⚙️ Quickstart Manual Deployment Loop

### 1. Provision Host Toolchains
Ensure your deployment machine context contains required compiler environments:
```bash
sudo apt-get update
sudo apt-get install -y g++ cmake sqlite3 libsqlite3-dev
```

### 2. Compile High-Speed Native Assets
Initialize your build workspace and compile optimized compilation binary targets using CMake:
```bash
mkdir -p build && cd build
cmake ..
cmake --build . --config Release
cd ..
```

### 3. Run Automated Validation Checks
Execute the continuous integration diagnostics matrix to verify operational boundaries:
```bash
pytest tests/test_main_core.py -v
```

### 4. Boot the Primary Orchestration Engine
Initialize the edge node runtime stack to activate the background data processing worker loops:
```bash
python3 main.py
```
*   **Interactive Viewport Panel:** Point your local web browser engine layout to `http://127.0.0.1:8000` to monitor live state traces, thoughts, and balancing metrics in real-time.
*   **Ingest Sensor Telemetry Packets:** Feed active real-world telemetry stream records directly into your tracking loops:
    ```bash
    curl -X POST "http://127.0.0" -H "Content-Type: application/json" -d '{"feedback_vector": 0.8421}'
    ```

---

## 🔄 Automated Backup Ledger Scheduling
To activate your hourly automated SQLite ledger history backups, add the following cron configuration line to your system layout settings via `crontab -e`:
```text
0 * * * * /bin/bash /absolute/path/to/kryptic-agent/backup_agent_ledger.sh
```

---

## 👤 Author & Enterprise Licensing
*   **Author:** Brandon Mark Wilson
*   **Contact:** mark.brandonwilson@gmail.com
*   **Repository:** [KrypticKode007/kryptic-agent](https://github.com/KrypticKode007/kryptic-agent)
*   **Licensing:** Open-source platform deployed under the standard Apache-2.0 open-source license agreements.
