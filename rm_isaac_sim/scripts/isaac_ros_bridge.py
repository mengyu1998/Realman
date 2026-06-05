#!/usr/bin/env python3
"""
RM65 Isaac Sim ROS2 桥接节点

功能:
1. 订阅真实机械臂的关节状态
2. 将关节状态发布到 Isaac Sim
3. 同步虚拟机械臂与真实机械臂的状态

使用方法:
ros2 run rm_isaac_sim isaac_ros_bridge
"""

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from sensor_msgs.msg import JointState
import threading


class IsaacRosBridge(Node):
    """Isaac Sim ROS2 桥接节点"""

    def __init__(self):
        super().__init__('isaac_ros_bridge')

        # QoS 配置
        self.qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )

        # 关节状态存储
        self.left_arm_state = None
        self.right_arm_state = None
        self.lock = threading.Lock()

        # 订阅真实机械臂的关节状态
        self.left_arm_sub = self.create_subscription(
            JointState,
            '/arm_left/joint_states',
            self.left_arm_callback,
            self.qos_profile
        )

        self.right_arm_sub = self.create_subscription(
            JointState,
            '/arm_right/joint_states',
            self.right_arm_callback,
            self.qos_profile
        )

        # 发布关节状态到 Isaac Sim
        self.left_arm_pub = self.create_publisher(
            JointState,
            '/arm_left/isaac_joint_states',
            self.qos_profile
        )

        self.right_arm_pub = self.create_publisher(
            JointState,
            '/arm_right/isaac_joint_states',
            self.qos_profile
        )

        # 创建定时器，定期发布关节状态
        self.timer = self.create_timer(0.01, self.publish_callback)  # 100 Hz

        self.get_logger().info('Isaac ROS Bridge 节点已启动')
        self.get_logger().info('订阅: /arm_left/joint_states, /arm_right/joint_states')
        self.get_logger().info('发布: /arm_left/isaac_joint_states, /arm_right/isaac_joint_states')

    def left_arm_callback(self, msg):
        """左臂关节状态回调"""
        with self.lock:
            self.left_arm_state = msg

    def right_arm_callback(self, msg):
        """右臂关节状态回调"""
        with self.lock:
            self.right_arm_state = msg

    def publish_callback(self):
        """定时发布关节状态"""
        with self.lock:
            # 发布左臂关节状态
            if self.left_arm_state is not None:
                self.left_arm_pub.publish(self.left_arm_state)

            # 发布右臂关节状态
            if self.right_arm_state is not None:
                self.right_arm_pub.publish(self.right_arm_state)

    def destroy_node(self):
        """清理资源"""
        self.get_logger().info('关闭 Isaac ROS Bridge 节点')
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)

    try:
        node = IsaacRosBridge()
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f'错误: {e}')
    finally:
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
