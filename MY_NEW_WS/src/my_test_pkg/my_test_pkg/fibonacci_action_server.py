import rclpy
from rclpy.action import ActionServer, GoalResponse, CancelResponse
from rclpy.node import Node

from my_custom_interfaces.action import Fibonacci


class FibonacciActionServer(Node):
    def __init__(self):
        super().__init__('fibonacci_action_server')
        self._action_server = ActionServer(
            self,
            Fibonacci,
            'fibonacci',
            execute_callback=self.execute_callback,
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback,
        )
        self.get_logger().info('Fibonacci 动作服务器已启动，等待客户端请求...')

    def goal_callback(self, goal_request):
        self.get_logger().info(f'收到目标请求: order={goal_request.order}')
        if goal_request.order <= 0:
            self.get_logger().warn('order 必须大于 0，拒绝该目标')
            return GoalResponse.REJECT
        return GoalResponse.ACCEPT

    def cancel_callback(self, goal_handle):
        self.get_logger().info('收到取消请求，允许取消')
        return CancelResponse.ACCEPT

    async def execute_callback(self, goal_handle):
        order = goal_handle.request.order
        self.get_logger().info(f'开始执行 Fibonacci 计算: order={order}')

        feedback_msg = Fibonacci.Feedback()
        feedback_msg.partial_sequence = [0, 1]
        feedback_msg.current_index = 1

        if order == 1:
            goal_handle.succeed()
            result = Fibonacci.Result()
            result.sequence = [0]
            result.success = True
            return result

        sequence = [0, 1]
        feedback_msg.partial_sequence = sequence.copy()
        goal_handle.publish_feedback(feedback_msg)

        for index in range(2, order):
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                result = Fibonacci.Result()
                result.sequence = sequence
                result.success = False
                self.get_logger().info('任务被取消，返回当前结果')
                return result

            next_value = sequence[-1] + sequence[-2]
            sequence.append(next_value)

            feedback_msg.partial_sequence = sequence.copy()
            feedback_msg.current_index = index
            goal_handle.publish_feedback(feedback_msg)
            self.get_logger().info(f'反馈: index={index}, sequence={sequence}')

        goal_handle.succeed()
        result = Fibonacci.Result()
        result.sequence = sequence
        result.success = True
        self.get_logger().info(f'执行完成: sequence={sequence}')
        return result


def main(args=None):
    rclpy.init(args=args)
    node = FibonacciActionServer()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()