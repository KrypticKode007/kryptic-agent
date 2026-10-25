#!/bin/bash
# ================================================================================
# KRYPTIC-AGENT PRODUCTION RELEASE BUILD AUTOMATION PLAYBOOK
# ================================================================================
set -e

RELEASE_VERSION="1.0.0"
BUILD_DIR="build"
DIST_DIR="kryptic-agent-edge-v${RELEASE_VERSION}"

echo "================================================================================"
echo "STARTING PRODUCTION PACKAGING LIFECYCLE FOR KRYPTIC-AGENT..."
echo "================================================================================"

# 1. Clean up old build contexts
echo "[+] Flushing historical compilation footprints..."
rm -rf ${BUILD_DIR} ${DIST_DIR} *.tar.gz
mkdir -p ${BUILD_DIR}
mkdir -p ${DIST_DIR}

# 2. Compile native high-speed C++ matrix acceleration binaries via CMake
echo "[+] Configuring high-speed compilation matrices via CMake..."
cd ${BUILD_DIR}
cmake -DCMAKE_BUILD_TYPE=Release ..
echo "[+] Compiling native C++ assets..."
cmake --build . --config Release
cd ..

# 3. Verify target assets exist in the execution workspace root
if [ ! -f "matrix_accelerator" ]; then
    echo "[-] CRITICAL ERROR: Native matrix_accelerator execution binary missing."
    exit 1
fi

# 4. Stage distribution package layouts
echo "[+] Staging runtime files into release distribution workspace..."
cp main.py ${DIST_DIR}/
cp llm_orchestrator.py ${DIST_DIR}/
cp matrix_accelerator ${DIST_DIR}/
cp backup_agent_ledger.sh ${DIST_DIR}/

# 5. Compress production runtime files into a downloadable tarball release
echo "[+] Compressing release assets into downloadable production tarball package..."
tar -czf kryptic-agent-edge-v${RELEASE_VERSION}.tar.gz ${DIST_DIR}

echo "================================================================================"
echo "[✔] BUILD PRODUCTION RUN SUCCESSFUL: kryptic-agent-edge-v${RELEASE_VERSION}.tar.gz is ready."
echo "================================================================================"
