cmake_minimum_required(VERSION 3.22)
project(KrypticAgentNativeCore VERSION 1.0.0 LANGUAGES CXX)

# Force strict compliance with C++17 compilation standards
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Configure advanced target compiler optimization vectors
if(MSVC)
    add_compile_options(/O2 /W4)
else()
    add_compile_options(-O3 -Wall -Wextra -ffast-math -march=native)
endif()

# Find systemic dependency packages
find_package(SQLite3 REQUIRED)

# Define native matrix accelerator executable mapping
add_executable(matrix_accelerator kryptic_hardware_accelerator.cpp)

# Bind linked include libraries and external definitions
target_include_directories(matrix_accelerator PRIVATE ${SQLite3_INCLUDE_DIRS})
target_link_libraries(matrix_accelerator PRIVATE ${SQLite3_LIBRARIES})

# Enforce clean executable deployment to repository root directory
set_target_properties(matrix_accelerator PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/.."
)
