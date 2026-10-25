# 1. Create a decoupled build caching workspace
mkdir -p build && cd build

# 2. Configure project files and native compiler vectors
cmake ..

# 3. Build and deploy optimized binaries to the root directory
cmake --build . --config Release

# 4. Step back to root and verify the target binary executes safely via Pytest
cd ..
pytest tests/test_main_core.py -v
