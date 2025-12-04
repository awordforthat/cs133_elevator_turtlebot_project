from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.conditions import IfCondition, UnlessCondition
from launch_ros.actions import Node
import os


def generate_launch_description():

    use_sim = LaunchConfiguration("use_sim")

    kobuki_sim_path = os.path.join(
        os.environ["HOME"],
        "ros2_kobuki_ws",
        "src",
        "kobuki_launch",
        "kobuki_launch",
        "launch",
        "kobuki_gazebo.launch.py",
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "use_sim",
                default_value="false",
                description="Run Gazebo simulation if true. If false, connect to real robot.",
            ),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(kobuki_sim_path),
                condition=IfCondition(use_sim),
            ),
            Node(
                package="elevator_proj",
                executable="control_node",
                name="control_node",
                output="screen",
            ),
            Node(
                package="elevator_proj",
                executable="speech_node",
                name="speech_node",
                output="screen",
            ),
            Node(
                package="elevator_proj",
                executable="screen_node",
                name="screen_node",
                output="screen",
            ),
            Node(
                package="kobuki_node",
                executable="kobuki_ros_node",
                name="kobuki",
                parameters=[
                    {"device_port": "/dev/ttyUSB0"},
                ],
                output="screen",
            ),
            Node(
                package="teleop_twist_keyboard",
                executable="teleop_twist_keyboard",
                name="teleop",
                prefix="xterm -e",
                remappings=[
                    ("/cmd_vel", "/commands/velocity"),
                ],
            ),
        ]
    )
