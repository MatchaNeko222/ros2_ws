import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import ParameterEvent
from rcl_interfaces.msg import ParameterType


class ParamListener(Node):
    """
    节点B：监听其他节点的参数变化
    订阅 /parameter_events，过滤出特定节点的事件
    """

    def __init__(self):
        super().__init__('param_listener')

        # 关键：订阅 /parameter_events 话题
        self.param_event_sub = self.create_subscription(
            ParameterEvent,
            '/parameter_events',
            self.on_parameter_event,
            10,
        )

        self.get_logger().info('✓ 参数监听节点已启动')
        self.get_logger().info('  (正在监听 /parameter_events 话题...)')

    def on_parameter_event(self, event: ParameterEvent):
        """
        接收参数事件
        event 的结构：
          - node: 更新参数的节点名
          - changed_parameters: 改变的参数列表
          - new_parameters: 新增的参数
          - deleted_parameters: 删除的参数
        """

        self.get_logger().info(f'收到参数事件: node={event.node}')

        # 只关注 param_publisher 节点的事件
        if event.node != 'param_publisher':
            return

        # 打印改变的参数
        if event.changed_parameters:
            self.get_logger().info(f'📍 [事件来自 {event.node}] 参数改变:')
            for param in event.changed_parameters:
                param_name = param.name
                param_value = param.value

                # ParameterValue 对象中包含不同类型的值字段
                if param_value.type == ParameterType.PARAMETER_DOUBLE:
                    val = param_value.double_value
                elif param_value.type == ParameterType.PARAMETER_INTEGER:
                    val = param_value.integer_value
                elif param_value.type == ParameterType.PARAMETER_BOOL:
                    val = param_value.bool_value
                elif param_value.type == ParameterType.PARAMETER_STRING:
                    val = param_value.string_value
                else:
                    val = f'<unsupported type={param_value.type}>'

                self.get_logger().info(f'   └─ {param_name} = {val}')

        # 打印新增的参数
        if event.new_parameters:
            self.get_logger().info(f'➕ [事件来自 {event.node}] 新参数声明:')
            for param in event.new_parameters:
                self.get_logger().info(f'   └─ {param.name}')

        # 打印删除的参数
        if event.deleted_parameters:
            self.get_logger().info(f'❌ [事件来自 {event.node}] 参数删除:')
            for param in event.deleted_parameters:
                self.get_logger().info(f'   └─ {param.name}')


def main(args=None):
    rclpy.init(args=args)
    node = ParamListener()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
