import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess

def generate_launch_description():
    gazebo_pkg_dir = get_package_share_directory('vla_gazebo')
    world_file = os.path.join(gazebo_pkg_dir, 'worlds', 'vla_world.sdf')
    
    # We export the GAZEBO_MODEL_PATH so it can find 'red_block'
    os.environ['GAZEBO_MODEL_PATH'] = os.path.join(gazebo_pkg_dir, 'models')
    
    return LaunchDescription([
        ExecuteProcess(
            cmd=['gazebo', '--verbose', world_file, '-s', 'libgazebo_ros_init.so', '-s', 'libgazebo_ros_factory.so'],
            output='screen'
        )
    ])
