# ================================================================================
# STAGE 1: HIGH-SPEED NATIVE BUILD ENVIRONMENT
# ================================================================================
FROM ubuntu:22.04 AS compiler-environment

# Enforce non-interactive backend compiler system installation configurations
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    g++ \
    cmake \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace_build
COPY CMakeLists.txt kryptic_hardware_accelerator.cpp ./

# Trigger compiler pass optimization profiles
RUN mkdir build && cd build && \
    cmake -DCMAKE_BUILD_TYPE=Release .. && \
    cmake --build . --config Release

# ================================================================================
# STAGE 2: PRODUCTION RUNTIME ENVIRONMENT
# ================================================================================
FROM python:3.10-slim AS runtime-environment

WORKDIR /app

# Install lightweight dependencies required by database runtimes
RUN apt-get update && apt-get install -y \
    sqlite3 \
    libsqlite3-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy packaged compilation artifacts from Stage 1 context
COPY --from=compiler-environment /matrix_accelerator /app/matrix_accelerator

# Deploy primary script manifests into container layout root
COPY main.py /app/main.py
COPY llm_orchestrator.py /app/llm_orchestrator.py
COPY backup_agent_ledger.sh /app/backup_agent_ledger.sh

# Install verified dependency frameworks via pip package infrastructure
RUN pip install --no-cache-dir fastapi uvicorn requests

# Expose local FastAPI stream tracking router port
EXPOSE 8000

# Set entry point parameters to boot the primary orchestration engine
CMD ["python", "main.py"]
