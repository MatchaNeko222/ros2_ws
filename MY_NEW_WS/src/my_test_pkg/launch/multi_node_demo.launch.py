from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='my_test_pkg',
            executable='multi_node_demo',
            output='screen',
        ),
    ])