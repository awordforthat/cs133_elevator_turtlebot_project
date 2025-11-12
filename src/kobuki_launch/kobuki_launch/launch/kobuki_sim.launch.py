from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node
import os

def generate_launch_description():
    urdf_file = os.path.join(
        os.environ['HOME'],
        'ros2_kobuki_ws',
        'src',
        'kobuki_ros',
        'kobuki_description',
        'urdf',
        'kobuki_gazebo.urdf'
    )

    world_file = os.path.join(
        os.environ['HOME'],
        'ros2_kobuki_ws',
        'src',
        'kobuki_launch',
        'worlds',
        'kobuki_world.sdf'
    )

    return LaunchDescription([
        # Launch Gazebo with your saved world
        ExecuteProcess(
            cmd=[
                'gazebo',
                '--verbose',
                world_file,
                '-s', 'libgazebo_ros_init.so',
                '-s', 'libgazebo_ros_factory.so'
            ],
            output='screen'
        ),

        # Spawn the robot model into Gazebo
        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            arguments=['-entity', 'kobuki', '-file', urdf_file],
            output='screen'
        ),

        # Optional: Start the ROS2 controller manager (for sim teleop)
        Node(
            package='controller_manager',
            executable='ros2_control_node',
            parameters=[urdf_file,
                        os.path.join(os.environ['HOME'], 'ros2_kobuki_ws', 'src', 'kobuki_launch', 'config', 'kobuki_controllers.yaml')],
            output='screen'
        ),
    ])
