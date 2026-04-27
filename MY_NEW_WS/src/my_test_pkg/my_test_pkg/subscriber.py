#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class SubscriberNode(Node):
    def __init__(self):
        super().__init__("subscriber_node")
        self.subscriber = self.create_subscription(
            String,
            "my_topic",
            self.callback,
            10
        )
        self.get_logger().info("订阅者已启动！")

    def callback(self, msg):
        self.get_logger().info("收到：" + msg.data)

def main(args=None):
    rclpy.init(args=args)
    node = SubscriberNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()