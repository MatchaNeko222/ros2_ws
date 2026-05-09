import rclpy
from rclpy.executors import MultiThreadedExecutor

from my_test_pkg.publisher import PublisherNode
from my_test_pkg.subscriber import SubscriberNode


def main(args=None):
    rclpy.init(args=args)

    publisher_node = PublisherNode()
    subscriber_node = SubscriberNode()

    executor = MultiThreadedExecutor()
    executor.add_node(publisher_node)
    executor.add_node(subscriber_node)

    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        executor.shutdown()
        publisher_node.destroy_node()
        subscriber_node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()