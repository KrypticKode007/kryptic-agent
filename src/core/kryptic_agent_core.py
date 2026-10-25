import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
from sensor_msgs.msg import JointState

class KrypticROS2Driver(Node):
    """Native ROS 2 Node interface mapping physical hardware registries."""
    def __init__(self, engine):
        super().__init__('kryptic_agent_hardware_bridge')
        self.engine = engine
        
        # Publisher sending active inference corrective vectors to the motor system
        self.actuation_pub = self.create_publisher(Float64MultiArray, '/hardware/motor_commands', 10)
        
        # Subscription tracking live raw joint encoders and telemetry feeds
        self.joint_sub = self.create_subscription(JointState, '/joint_states', self.callback, 10)
        self.current_positions = [0.0] * engine.num_joints
        self.current_velocities = [0.0] * engine.num_joints

    def callback(self, msg: JointState):
        """Captures real-time multi-axis positions directly from physical actuators."""
        self.current_positions = list(msg.position[:self.engine.num_joints])
        self.current_velocities = list(msg.velocity[:self.engine.num_joints])

    def publish_actuation_vectors(self, commands: list):
        """Dispatches minimized free energy gradients directly to physical motor drivers."""
        msg = Float64MultiArray()
        msg.data = commands
        self.actuation_pub.publish(msg)
      
