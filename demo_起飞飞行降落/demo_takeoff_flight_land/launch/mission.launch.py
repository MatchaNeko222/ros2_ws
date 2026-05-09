from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription(
        [
            Node(
                package="demo_takeoff_flight_land",
                executable="mission_node",
                name="mission_node",
                output="screen",
            )
        ]
    )
