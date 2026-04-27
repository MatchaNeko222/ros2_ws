import rclpy
from rcl_interfaces.msg import SetParametersResult
from rclpy.node import Node

from my_custom_interfaces.msg import PersonInfo


class PersonInfoParamPublisher(Node):
    def __init__(self):
        # 1) 创建节点
        super().__init__('person_info_param_publisher')

        # 2) 声明参数（声明后才能被ros2 param读取和修改）
        self.declare_parameter('topic_name', 'person_info_param')
        self.declare_parameter('publish_period', 10.0)
        self.declare_parameter('default_name', 'Luckiop')
        self.declare_parameter('default_age', 20)

        # 3) 读取参数并保存到类成员变量，供后续逻辑使用
        self.topic_name = self.get_parameter('topic_name').value
        self.publish_period = float(self.get_parameter('publish_period').value)
        self.default_name = self.get_parameter('default_name').value
        self.default_age = int(self.get_parameter('default_age').value)

        # 4) 用参数创建发布器和定时器
        self.publisher_ = self.create_publisher(PersonInfo, self.topic_name, 10)
        self.timer = self.create_timer(self.publish_period, self.timer_callback)
        self.count = 0

        # 5) 注册参数回调，实现运行时动态改参
        self.add_on_set_parameters_callback(self.on_parameters_changed)

        self.get_logger().info(
            f'节点已启动: topic={self.topic_name}, period={self.publish_period}, '
            f'name={self.default_name}, age={self.default_age}'
        )

    def on_parameters_changed(self, params):
        # 参数校验与更新逻辑：这里只允许动态改发布周期、默认姓名和默认年龄
        for param in params:
            if param.name == 'publish_period':
                if param.value <= 0.0:
                    return SetParametersResult(
                        successful=False,
                        reason='publish_period 必须大于 0',
                    )
            if param.name == 'default_age':
                if param.value < 0 or param.value > 120:
                    return SetParametersResult(
                        successful=False,
                        reason='default_age 必须在 0~120 之间',
                    )

        for param in params:
            if param.name == 'publish_period':
                self.publish_period = float(param.value)
                # 重新创建定时器，让新周期立即生效
                self.timer.cancel()
                self.timer = self.create_timer(self.publish_period, self.timer_callback)
            elif param.name == 'default_name':
                self.default_name = str(param.value)
            elif param.name == 'default_age':
                self.default_age = int(param.value)

        self.get_logger().info(
            f'参数已更新: period={self.publish_period}, name={self.default_name}, age={self.default_age}'
        )
        return SetParametersResult(successful=True)

    def timer_callback(self):
        # 6) 使用参数值构造并发布自定义消息
        msg = PersonInfo()
        msg.name = f'{self.default_name}_{self.count}'
        msg.age = self.default_age
        msg.email = f'{self.default_name.lower()}_{self.count}@example.com'
        msg.phone = f'1380000{1000 + self.count}'

        self.publisher_.publish(msg)
        self.get_logger().info(
            f'发布消息 -> name={msg.name}, age={msg.age}, email={msg.email}, phone={msg.phone}'
        )
        self.count += 1


def main(args=None):
    rclpy.init(args=args)
    node = PersonInfoParamPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()