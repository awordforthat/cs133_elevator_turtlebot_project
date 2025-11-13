from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='elevator_proj',
            executable='control_node',
            name='control_node',
            output='screen'
        ),
        Node(
            package='elevator_proj',
            executable='speech_node',
            name='speech_node',
            output='screen'
        ),
        Node(
            package='elevator_proj',
            executable='screen_node',
            name='screen_node',
            output='screen'
        ),
    ])
