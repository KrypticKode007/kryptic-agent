# Kryptic-Agent

Kryptic-Agent is a Python/C++ robotics and active-inference runtime with a ROS 2-compatible interface, FastAPI telemetry dashboard, and CMake C++ latency harness.

## Repository status

This repository is organized as a Python-first runtime with a C++ validation target. It is intentionally rooted at the repository root so imports and local execution work without installation packaging churn.

## Prerequisites

- Python 3.10+
- CMake 3.16+
- GCC/Clang
- `pip`

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Validation and build

From the repository root:

```bash
python -m compileall .
pytest tests -q
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --parallel
```

## Runtime entrypoints

Python runtime:

```bash
python main.py
```

If you want to use the Cyclone DDS configuration:

```bash
export CYCLONE_DDS_URI="$PWD/cyclone_dds_config.xml"
python main.py
```

The repository also contains the legacy design notes in `master_kryptic_monolith.md`; those are documentation artifacts and are not the active executable entrypoint.

## Project layout

- `main.py` — FastAPI runtime and orchestration entrypoint
- `kryptic_integration_core.py` — homeostatic and safety integration pipeline
- `ego_boundary_calculator.py` — boundary classification calculator
- `encrypt_weights.py` — AES-GCM weight encryption wrapper
- `CMakeLists.txt` — C++ build configuration
- `test_hardware_latency.cpp` — C++ latency verification target
- `tests/` — Python test suite

## Notes

- The project intentionally does not use a Node/Vitest toolchain.
- The repo root is the runtime root; avoid moving the code into a nested package before the build is finalized.
- Local database artifacts (for example `tracking_profiles.db`, `kryptic_history.db`) remain ignored and should not be committed.
