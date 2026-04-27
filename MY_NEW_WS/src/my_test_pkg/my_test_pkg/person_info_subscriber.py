import rclpy
from rclpy.node import Node
from my_custom_interfaces.msg import PersonInfo

class PersonInfoSubscriber(Node):
    def __init__(self):
        super().__init__('person_info_subscriber')
        self.subscription = self.create_subscription(
            PersonInfo,
            'person_info',
            self.listener_callback,
            10)
        self.subscription  # 防止未被引用被垃圾回收

    def listener_callback(self, msg):
        self.get_logger().info(
            f'收到: name={msg.name}, age={msg.age}, email={msg.email}, phone={msg.phone}')

def main(args=None):
    rclpy.init(args=args)
    node = PersonInfoSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
