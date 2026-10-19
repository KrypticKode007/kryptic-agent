#!/usr/bin/env python3
"""
Module: kryptic_edge_launch.py
Branch: commercial/production-edge-architecture

ROS 2 Launch script prototype initializing the self-healing homeostatic edge layers 
and safety monitor nodes automatically on flight computer startup.
"""

from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # 1. Core Homeostatic Self-Healing Safety Layer Node
        Node(
            package='kryptic_agent',
            executable='kryptic_ros2_edge_core',
            name='kryptic_edge_ros_node',
            output='screen',
            emulate_tty=True,
            parameters=[{
                'min_battery_threshold': 20.0,
                'max_allowable_g_force': 30.0,
                'flash_ledger_path': 'kryptic_flash_ledger.bin'
            }],
            remappings=[
                ('/drone/battery', '/hardware/telemetry/battery'),
                ('/drone/imu', '/hardware/telemetry/imu')
            ]
        ),
        
        # 2. Kinetic Failsafe Mediator Actuator Node
        Node(
            package='kryptic_agent',
            executable='kinetic_failsafe_mediator',
            name='kinetic_failsafe_mediator_node',
            output='screen',
            parameters=[{
                'auto_land_descent_rate': 1.5
            }]
        )
    ])
          
