# filename: CMakeLists.txt
cmake_minimum_required(VERSION 3.8)
project(kryptic_hardware_core)

if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
endif()

# Strict bare-metal compilation optimization flags
if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(
    -O3                    # Enable maximum code execution speed optimization
    -march=native          # Optimize instructions explicitly for the host system chip
    -ffast-math            # Bypass strict IEEE math compliance for hyper-fast vector math
    -Wall -Wextra -Werror  # Strict build warning enforcement
  )
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)

# Link native POSIX real-time system tracking library (-lrt)
link_libraries(rt)

add_executable(robotic_sentience_core src/robotic_sentience_core.cpp)
target_link_libraries(robotic_sentience_core PRIVATE rclcpp std_msgs)

ament_package()
