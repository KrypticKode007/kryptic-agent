#!/usr/bin/env python3
"""
Kryptic-Agent ROS 2 Hardware System Launch Lifecycle Driver
Configures parameters, lifecycle states, and node linkages for the physical lab setup.
"""

import os
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    # Define production parameters for real-time inference tracking loops
    hardware_parameters = {
        "num_joints": 4,
        "precision_scale_factor": 10.0,
        "max_actuation_torque": 4.5,
        "fallback_simulation_mode": False
    }

    # Configuration block instantiation for the native ROS 2 physical driver node
    kryptic_hardware_node = Node(
        package='kryptic_agent',
        executable='kryptic_agent_core.py',
        name='kryptic_agent_hardware_bridge',
        namespace='kryptic',
        output='screen',
        parameters=[hardware_parameters],
        remappings=[
            ('/joint_states', '/hardware/joint_states'),
            ('/hardware/motor_commands', '/hardware/actuation_vectors')
        ]
    )

    return LaunchDescription([
        kryptic_hardware_node
    ])
  
