# CMakeLists.txt
# Cross-compilation build layout matrix for the bare-metal C++ latency tracker.
cmake_minimum_required(VERSION 3.16)
project(kryptic_hardware_core CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Enforce explicit embedded hardware optimization parameters
if(CMAKE_COMPILER_IS_GNUCXX)
    add_compile_options(-O3 -Wall -Wextra -Wpedantic -ffast-math -fno-exceptions -fno-rtti)
endif()

# 1. Define the Latency Test Executable Target Binary
add_executable(test_hardware_latency test_hardware_latency.cpp)

# 2. Explicitly map system include pathways
target_include_directories(test_hardware_latency PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})

# 3. Add test registration suite capabilities
enable_testing()
add_test(NAME InvariantOverheadTest COMMAND test_hardware_latency)
