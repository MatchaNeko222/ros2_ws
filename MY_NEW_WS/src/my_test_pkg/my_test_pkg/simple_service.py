import rclpy  # 导入ROS2 Python库
from rclpy.node import Node  # 导入Node基类
from my_test_interfaces.srv import AddThreeInts  # 导入自定义的加法服务类型

# 定义服务端节点
class AddThreeIntsService(Node):
    def __init__(self):
        super().__init__('add_three_ints_service')  # 节点名
        # 创建服务，类型为AddThreeInts，服务名为'add_three_ints'
        self.srv = self.create_service(AddThreeInts, 'add_three_ints', self.add_three_ints_callback)
        self.get_logger().info('三整数加法服务端已启动！')

    # 回调函数，收到请求时自动调用
    def add_three_ints_callback(self, request, response):
        self.get_logger().info(f'收到请求: {request.a} + {request.b} + {request.c}')
        response.sum = request.a + request.b + request.c  # 计算结果
        return response  # 返回应答

def main(args=None):
    rclpy.init(args=args)
    node = AddThreeIntsService()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()