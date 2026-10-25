cmake_minimum_required(VERSION 3.16)
project(kryptic_hardware_core LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

if(CMAKE_CXX_COMPILER_ID STREQUAL "GNU" OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
    add_compile_options(-O3 -Wall -Wextra -Wpedantic)
endif()

add_executable(kryptic_hardware_accelerator
    kryptic_hardware_accelerator.cpp
)

target_include_directories(kryptic_hardware_accelerator
    PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}
)

add_executable(test_hardware_latency
    test_hardware_latency.cpp
)

target_include_directories(test_hardware_latency
    PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}
)
