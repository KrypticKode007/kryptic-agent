# AGENTS.md

## Project overview

This repository is a Python-first robotics and active-inference runtime with a C++ validation target. The source root is the repository root itself. Keep the runtime rooted there unless the project is deliberately restructured.

## Build and test commands

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m compileall .
pytest tests -q
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --parallel
```

## Important constraints

- Do not reintroduce a Node/Vitest toolchain unless the project is explicitly converted to a JS package.
- Do not add repo-root imports that assume a nested package layout.
- Keep `main.py`, `kryptic_integration_core.py`, `ego_boundary_calculator.py`, and `encrypt_weights.py` valid at the root.
- Treat legacy marketing and proposal files as documentation only unless a runtime entrypoint is explicitly added.
