import os
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
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
        # Node(
        #     package='vla_execution',
        #     executable='moveit_wrapper_node',
        #     name='moveit_wrapper_node',
        #     output='screen',
        # )
    ])
