import rclpy
from rclpy.node import Node
from my_custom_interfaces.msg import PersonInfo

class PersonInfoPublisher(Node):
    def __init__(self):
        super().__init__('person_info_publisher')
        self.publisher_ = self.create_publisher(PersonInfo, 'person_info', 10)
        timer_period = 2.0  # 每2秒发布一次
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.count = 0

    def timer_callback(self):
        msg = PersonInfo()
        msg.name = f'User{self.count}'
        msg.age = 20 + self.count
        msg.email = f'user{self.count}@example.com'
        msg.phone = f'1380000{1000 + self.count}'
        self.publisher_.publish(msg)
        self.get_logger().info(f'发布: {msg.name}, {msg.age}, {msg.email}, {msg.phone}')
        self.count += 1

def main(args=None):
    rclpy.init(args=args)
    node = PersonInfoPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
