from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    publisher_node = Node(
        package='my_test_pkg',
        executable='publisher',
        name='publisher_node',
        output='screen',
    )

    subscriber_node = Node(
        package='my_test_pkg',
        executable='subscriber',
        name='subscriber_node',
        output='screen',
    )

    return LaunchDescription([
        publisher_node,
        subscriber_node,
    ])
