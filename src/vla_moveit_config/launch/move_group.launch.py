import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from moveit_configs_utils import MoveItConfigsBuilder

def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    moveit_config = (
        MoveItConfigsBuilder("vla_arm", package_name="vla_moveit_config")
        .robot_description(file_path="config/vla_arm.urdf.xacro")
        .robot_description_semantic(file_path="config/vla_arm.srdf")
        .trajectory_execution(file_path="config/moveit_controllers.yaml")
        .planning_pipelines(pipelines=["ompl"])
        .to_moveit_configs()
    )
    
    # We explicitly inject use_sim_time into the parameter dictionary
    moveit_params = moveit_config.to_dict()
    moveit_params['use_sim_time'] = use_sim_time

    move_group_node = Node(
        package="moveit_ros_move_group",
        executable="move_group",
        output="screen",
        parameters=[moveit_params],
    )

    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='true', description='Use simulation (Gazebo) clock'),
        move_group_node
    ])
