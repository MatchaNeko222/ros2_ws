import sys

import rclpy
from action_msgs.msg import GoalStatus
from rclpy.action import ActionClient
from rclpy.node import Node

from my_custom_interfaces.action import Fibonacci


class FibonacciActionClient(Node):
    def __init__(self):
        super().__init__('fibonacci_action_client')
        self._action_client = ActionClient(self, Fibonacci, 'fibonacci')

    def send_goal(self, order: int):
        self.get_logger().info(f'准备发送目标: order={order}')
        self._action_client.wait_for_server()

        goal_msg = Fibonacci.Goal()
        goal_msg.order = order

        send_goal_future = self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback,
        )
        send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().warn('目标被服务器拒绝')
            rclpy.shutdown()
            return

        self.get_logger().info('目标已被接受，等待结果...')
        get_result_future = goal_handle.get_result_async()
        get_result_future.add_done_callback(self.get_result_callback)

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info(
            f'反馈: index={feedback.current_index}, partial={list(feedback.partial_sequence)}'
        )

    def get_result_callback(self, future):
        response = future.result()
        status = response.status
        result = response.result

        if status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info(
                f'结果成功: success={result.success}, sequence={list(result.sequence)}'
            )
        else:
            self.get_logger().warn(
                f'结果状态非成功(status={status}): success={result.success}, '
                f'sequence={list(result.sequence)}'
            )

        rclpy.shutdown()


def main(args=None):
    rclpy.init(args=args)
    node = FibonacciActionClient()

    order = 10
    if len(sys.argv) > 1:
        try:
            order = int(sys.argv[1])
        except ValueError:
            node.get_logger().warn('命令行参数无效，使用默认 order=10')

    node.send_goal(order)
    rclpy.spin(node)
    node.destroy_node()


if __name__ == '__main__':
    main()