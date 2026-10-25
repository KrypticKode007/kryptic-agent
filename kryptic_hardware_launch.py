import os
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    """
    Configures and spawns bare-metal physical hardware interface nodes 
    with high-velocity Cyclone DDS networking constraints.
    """
    # Force Cyclone DDS as the exclusive real-time multi-process transport middleware
    os.environ['RMW_IMPLEMENTATION'] = 'rmw_cyclonedds_cpp'
    
    # Optimize local network boundaries for zero packet drop at 1000Hz
    os.environ['CYCLONEDDS_URI'] = """<CycloneDDS>
        <Domain id="any">
            <General>
                <NetworkInterfaceAddress>lo</NetworkInterfaceAddress>
                <AllowMulticast>false</AllowMulticast>
            </General>
            <Internal>
                <Watermarks>
                    <Whigh>5242880</Whigh>
                </Watermarks>
            </Internal>
        </Domain>
    </CycloneDDS>"""

    # Primary hardware node orchestration mapping
    hardware_driver_node = Node(
        package='kryptic_agent_drivers',
        executable='physical_encoder_bridge',
        name='hardware_io_bridge',
        output='screen',
        parameters=[{
            'use_sim_time': False,  # STRIP SIMULATION TIME; FORCE LOCAL HARDWARE CLOCK
            'serial_baudrate': 1152000,
            'update_rate_hz': 1000
        }]
    )

    # Active Inference Cybernetic Processing Engine Node
    sentience_core_node = Node(
        package='kryptic_agent_core',
        executable='robotic_sentience_core',
        name='vfe_matrix_engine',
        output='screen',
        prefix=['sudo -E env "PATH=$PATH"'], # Elevates process for POSIX FIFO scheduler access
        parameters=[{
            'use_sim_time': False,
            'axis_count': 6,
            'precision_mode': 'high'
        }]
    )

    return LaunchDescription([
        hardware_driver_node,
        sentience_core_node
    ])
    
