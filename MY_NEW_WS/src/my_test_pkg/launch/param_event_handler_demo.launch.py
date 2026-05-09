from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='my_test_pkg',
            executable='param_event_handler_demo',
            output='screen',
            parameters=[
                {'message': 'Hello from ParameterEventHandler'},
                {'publish_period': 2.0},
                {'counter': 0},
            ],
        ),
    ])
