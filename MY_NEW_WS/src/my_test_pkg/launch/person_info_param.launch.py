from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    # 启动参数可在命令行覆盖，例如 publish_period:=5.0
    topic_name_arg = DeclareLaunchArgument(
        'topic_name',
        default_value='person_info_param',
        description='发布PersonInfo消息的话题名',
    )
    publish_period_arg = DeclareLaunchArgument(
        'publish_period',
        default_value='10.0',
        description='消息发布周期（秒）',
    )
    default_name_arg = DeclareLaunchArgument(
        'default_name',
        default_value='Luckiop',
        description='默认姓名前缀',
    )
    default_age_arg = DeclareLaunchArgument(
        'default_age',
        default_value='20',
        description='默认年龄',
    )

    param_publisher = Node(
        package='my_test_pkg',
        executable='person_info_param_publisher',
        name='person_info_param_publisher',
        output='screen',
        parameters=[{
            'topic_name': LaunchConfiguration('topic_name'),
            'publish_period': LaunchConfiguration('publish_period'),
            'default_name': LaunchConfiguration('default_name'),
            'default_age': LaunchConfiguration('default_age'),
        }],
    )

    return LaunchDescription([
        topic_name_arg,
        publish_period_arg,
        default_name_arg,
        default_age_arg,
        param_publisher,
    ])
