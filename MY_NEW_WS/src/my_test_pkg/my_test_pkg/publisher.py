#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import datetime  # 新增：导入时间模块

class PublisherNode(Node):
    def __init__(self):
        super().__init__("publisher_node")
        self.publisher = self.create_publisher(String, "my_topic", 10)
        self.timer = self.create_timer(0.5, self.timer_callback)
        self.get_logger().info("发布者已启动！")

    def timer_callback(self):
        msg = String()
        # 获取当前时间并转为字符串
        msg.data = str(datetime.datetime.now())
        self.publisher.publish(msg)
        self.get_logger().info(f"已发布: {msg.data}")

def main(args=None):
    rclpy.init(args=args)
    node = PublisherNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()