import rclpy
from rclpy.node import Node
from my_test_interfaces.srv import AddThreeInts

class AddThreeIntsClient(Node):
    def __init__(self):
        super().__init__('add_three_ints_client')
        self.client = self.create_client(AddThreeInts, 'add_three_ints')
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('等待服务端上线...')
        self.request = AddThreeInts.Request()

    def send_request(self, a, b, c):
        self.request.a = a
        self.request.b = b
        self.request.c = c
        future = self.client.call_async(self.request)
        rclpy.spin_until_future_complete(self, future)
        if future.result() is not None:
            self.get_logger().info(f'应答: {future.result().sum}')
        else:
            self.get_logger().error('服务调用失败')

def main(args=None):
    rclpy.init(args=args)
    node = AddThreeIntsClient()
    node.send_request(114, 514, 1919)  # 这里可以改成你想加的三个数
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()