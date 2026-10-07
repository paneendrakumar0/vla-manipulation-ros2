import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('vla_gazebo'), 'launch', 'sim.launch.py')
        )
    )

    return LaunchDescription([
        gazebo_launch,
        Node(
            package='vla_perception',
            executable='vlm_node',
            name='vlm_node',
            output='screen',
        ),
        Node(
            package='vla_spatial',
            executable='spatial_node',
            name='spatial_node',
            output='screen',
        ),
        Node(
            package='vla_execution',
            executable='moveit_wrapper_node',
            name='moveit_wrapper_node',
            output='screen',
        )
    ])
