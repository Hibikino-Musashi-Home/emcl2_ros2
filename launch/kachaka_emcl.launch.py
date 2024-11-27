import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, GroupAction
from launch.substitutions import LaunchConfiguration, TextSubstitution
from launch_ros.actions import Node, SetParameter


def generate_launch_description():
    params_file = LaunchConfiguration('params_file')
    use_sim_time = LaunchConfiguration('use_sim_time')

    declare_use_sim_time = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation (Gazebo) clock if true')
    declare_params_file = DeclareLaunchArgument(
        'params_file',
        default_value=[
            TextSubstitution(text=os.path.join(
                get_package_share_directory('emcl2'), 'config', '')),
            TextSubstitution(text='emcl2.param.yaml')],
        description='emcl2 param file path')

    launch_node = GroupAction(
        actions=[
            SetParameter('use_sim_time', use_sim_time),
            Node(
                name='emcl2',
                package='emcl2',
                executable='emcl2_node',
                parameters=[params_file],
                remappings=[('scan', '/kachaka/lidar/scan'), ('map', '/kachaka/mapping/map')],
                output='screen'),
        ]
    )

    ld = LaunchDescription()
    ld.add_action(declare_use_sim_time)
    ld.add_action(declare_params_file)

    ld.add_action(launch_node)

    return ld

