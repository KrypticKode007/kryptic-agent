#!/usr/bin/env python3
"""ROS 2 compatibility layer for edge execution without the ROS 2 runtime installed."""

try:
    import rclpy
    from rclpy.node import Node
    from std_msgs.msg import Float64MultiArray
    from sensor_msgs.msg import JointState
except ImportError:  # pragma: no cover - this is a runtime fallback for minimal environments
    rclpy = None
    Node = object
    Float64MultiArray = None
    JointState = None


class KrypticROS2Driver(Node):
    """Native ROS 2 Node interface mapping physical hardware registries."""

    def __init__(self, engine):
        self.engine = engine
        self.current_positions = [0.0] * getattr(engine, "num_joints", 4)
        self.current_velocities = [0.0] * getattr(engine, "num_joints", 4)

        if rclpy is None or Node is object:
            self._fallback_mode = True
            return

        self._fallback_mode = False
        super().__init__("kryptic_agent_hardware_bridge")
        self.actuation_pub = self.create_publisher(Float64MultiArray, "/hardware/motor_commands", 10)
        self.joint_sub = self.create_subscription(JointState, "/joint_states", self.callback, 10)

    def callback(self, msg):
        if self._fallback_mode:
            return
        self.current_positions = list(msg.position[: self.engine.num_joints])
        self.current_velocities = list(msg.velocity[: self.engine.num_joints])

    def publish_actuation_vectors(self, commands):
        if self._fallback_mode:
            return
        msg = Float64MultiArray()
        msg.data = commands
        self.actuation_pub.publish(msg)
