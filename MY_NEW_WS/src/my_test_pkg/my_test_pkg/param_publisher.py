import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter
import time


class ParamPublisher(Node):
    """
    节点A：定期改变自己的参数，模拟无人机控制参数变化
    """

    def __init__(self):
        super().__init__('param_publisher')

        # 声明参数
        self.declare_parameter('speed', 0.0)
        self.declare_parameter('altitude', 0.0)
        self.declare_parameter('battery_level', 100)

        self.get_logger().info('✓ 参数发布节点已启动')
        self.get_logger().info('  (B节点将监听我的参数变化)')

        # 定时改参数
        self.update_count = 0
        self.timer = self.create_timer(2.0, self.update_params)

    def update_params(self):
        """每2秒改变参数"""
        self.update_count += 1

        # 模拟各种参数变化
        if self.update_count % 3 == 1:
            new_speed = (self.update_count * 0.5) % 10.0
            self.set_parameters([Parameter('speed', Parameter.Type.DOUBLE, new_speed)])
            self.get_logger().info(f'[A节点] 改变 speed -> {new_speed}')

        elif self.update_count % 3 == 2:
            new_altitude = (self.update_count * 2.0) % 50.0
            self.set_parameters([Parameter('altitude', Parameter.Type.DOUBLE, new_altitude)])
            self.get_logger().info(f'[A节点] 改变 altitude -> {new_altitude}')

        else:
            new_battery = max(0, 100 - self.update_count * 3)
            self.set_parameters([Parameter('battery_level', Parameter.Type.INTEGER, new_battery)])
            self.get_logger().info(f'[A节点] 改变 battery_level -> {new_battery}')


def main(args=None):
    rclpy.init(args=args)
    node = ParamPublisher()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
