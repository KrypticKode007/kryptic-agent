cmake_minimum_required(VERSION 3.10)
project(kryptic_hardware_suite CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Force aggressive native compilation optimizations and thread flags
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O3 -march=native -pthread -Wall -Wextra")

# Locate ROS 2 and hardware component links if required
find_package(rclcpp REQUIRED)

add_executable(test_hardware_latency test_hardware_latency.cpp)

# Link targeted system POSIX real-time extensions for sub-millisecond clock tracking
target_link_libraries(test_hardware_latency 
    PRIVATE 
    rclcpp::rclcpp
    rt # Explicitly binds POSIX real-time library (-lrt)
)
