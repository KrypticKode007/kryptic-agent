import os
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    # Target physical UART / Serial node on physical hardware lines
    # Jetson Orin UARTs typically expose via /dev/ttyTHS* lines
    hardware_telemetry_port = os.getenv('KRYPTIC_HARDWARE_PORT', '/dev/ttyTHS1')

    return LaunchDescription([
        Node(
            package='kryptic_agent',
            executable='kryptic_ros2_edge_core.py',
            name='kryptic_ros2_edge_core',
            output='screen',
            parameters=[{
                'hardware_port': hardware_telemetry_port,
                'use_realtime_priority': True,
                'fault_isolation_timeout_ms': 1.0
            }],
            # Elevate process boundaries to prevent OS-level scheduling jitter
            prefix=['chrt --rr 99'], 
            remappings=[]
        ),
        Node(
            package='kryptic_agent',
            executable='kinetic_failsafe_mediator',
            name='kinetic_failsafe_mediator',
            output='screen',
            parameters=[{
                'recovery_routine_active': True
            }]
        )
    ])
  
