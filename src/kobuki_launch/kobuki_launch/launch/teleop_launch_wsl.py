from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription(
        [
            Node(
                package="kobuki_node",
                executable="kobuki_ros_node",
                name="kobuki_node",
                output="screen",
                parameters=[{"device_port": "/dev/ttyUSB0"}, {"baudrate": 115200}],
            ),
            # Start teleop
            Node(
                package="teleop_twist_keyboard",
                executable="teleop_twist_keyboard",
                prefix="xterm -e",
                output="screen",
            ),
        ]
    )
