import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter

from std_msgs.msg import String
from rcl_interfaces.msg import ParameterEvent


class ParamEventHandlerDemo(Node):
    """
    演示参数事件监听（事件驱动）
    通过订阅 /parameter_events 话题来监听**所有节点**的参数变化
    这是 ROS 2 参数系统的底层机制

    优势：
    - 可以跨节点监听参数
    - 完全事件驱动
    - 看得到参数系统的微观运作
    """

    def __init__(self):
        super().__init__('param_event_handler_demo')

        # 声明参数
        self.declare_parameter('message', 'Hello ROS2')
        self.declare_parameter('publish_period', 1.0)
        self.declare_parameter('counter', 0)

        # 创建发布器
        self.publisher_ = self.create_publisher(String, 'param_demo_topic', 10)
        self.timer = self.create_timer(
            self.get_parameter('publish_period').value,
            self.timer_callback,
        )

        # 初始化参数值
        self.message = self.get_parameter('message').value

        # 关键：直接订阅 /parameter_events 话题
        # 这会收到系统里**任何节点**的参数变化事件
        self.param_event_sub = self.create_subscription(
            ParameterEvent,
            '/parameter_events',
            self.on_parameter_event,
            10,
        )

        self.get_logger().info('✓ 参数事件监听器已启动（事件驱动）')
        self.get_logger().info(
            f'初始参数: message="{self.message}", '
            f'publish_period={self.get_parameter("publish_period").value}, '
            f'counter={self.get_parameter("counter").value}'
        )

    def on_parameter_event(self, event: ParameterEvent):
        """
        接收参数事件消息
        event 包含：
        - timestamp: 事件时间戳
        - node: 触发参数变化的节点名
        - changed_parameters: 本次改变的参数列表
        - new_parameters: 新增的参数
        - deleted_parameters: 删除的参数
        """

        # 只处理本节点的参数变化
        if event.node != self.get_name():
            return

        # 处理已改变的参数
        for changed_param in event.changed_parameters:
            param_name = changed_param.name
            param_value = changed_param.value

            self.get_logger().info(
                f'[ParameterEvent] "{param_name}" 已改变 -> value={param_value.string_value}'
            )

            if param_name == 'message':
                self.message = param_value.string_value

            elif param_name == 'publish_period':
                new_period = float(param_value.double_value)
                self.get_logger().info(
                    f'  -> 重建定时器，发布周期改为 {new_period} 秒'
                )
                self.timer.cancel()
                self.timer = self.create_timer(new_period, self.timer_callback)

            elif param_name == 'counter':
                counter_val = int(param_value.integer_value)
                self.get_logger().info(f'  -> counter 已更新为 {counter_val}')

        # 处理新增的参数
        if event.new_parameters:
            for new_param in event.new_parameters:
                self.get_logger().info(f'[ParameterEvent] 新参数 "{new_param.name}" 已声明')

        # 处理删除的参数
        if event.deleted_parameters:
            for deleted_param in event.deleted_parameters:
                self.get_logger().info(f'[ParameterEvent] 参数 "{deleted_param.name}" 已删除')

    def timer_callback(self):
        """定时发送消息"""
        counter = self.get_parameter('counter').value
        msg = String()
        msg.data = f'{self.message} (count={counter})'
        self.publisher_.publish(msg)
        self.get_logger().info(f'已发布: {msg.data}')

        # 更新计数参数，会自动触发参数事件
        new_counter = counter + 1
        self.set_parameters([Parameter('counter', Parameter.Type.INTEGER, new_counter)])


def main(args=None):
    rclpy.init(args=args)
    node = ParamEventHandlerDemo()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
