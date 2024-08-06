import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, GroupAction
from launch.substitutions import LaunchConfiguration, TextSubstitution
from launch_ros.actions import Node, SetParameter


def generate_launch_description():
    params_file = LaunchConfiguration('params_file')
    map_yaml_file = LaunchConfiguration('map')
    use_sim_time = LaunchConfiguration('use_sim_time')
    map_topic_name = LaunchConfiguration('map_topic_name')
    namespace = LaunchConfiguration('namespace')

    declare_map_yaml = DeclareLaunchArgument(
        'map',
        default_value=[
            TextSubstitution(text=os.path.join(
                get_package_share_directory('emcl2'), 'config', 'map', 'map_turtlebot_house.yaml'))],
        description='Full path to map yaml file to load')
    
    declare_use_sim_time = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation (Gazebo) clock if true')
    
    declare_params_file = DeclareLaunchArgument(
        'params_file',
        default_value=[
            TextSubstitution(text=os.path.join(
                get_package_share_directory('emcl2'), 'config', 'param', 'emcl2.param.yaml'))],
        description='emcl2 param file path')
    
    declare_map_topic_name = DeclareLaunchArgument(
        'map_topic_name', 
        default_value=TextSubstitution(text='map'), 
        description='map topic name'
    )
    
    declare_namespace = DeclareLaunchArgument(
        'namespace', 
        default_value=TextSubstitution(text='')
    )

    lifecycle_nodes = ['map_server']
    emcl2_map_topic = (namespace, '/', map_topic_name)
    launch_node = GroupAction(
        actions=[
            SetParameter('use_sim_time', use_sim_time),
            Node(
                namespace=namespace,
                package='nav2_map_server',
                executable='map_server',
                name='map_server',
                parameters=[{'yaml_filename': map_yaml_file}],
                output='screen', 
                remappings=[('map', map_topic_name)]
                ),
            Node(
                name='emcl2',
                package='emcl2',
                executable='emcl2_node',
                parameters=[params_file],
                output='screen', 
                remappings=[('map', emcl2_map_topic)]
                ),
            Node(
                namespace=namespace, 
                package='nav2_lifecycle_manager',
                executable='lifecycle_manager',
                name='lifecycle_manager_localization',
                output='screen',
                parameters=[{'autostart': True},
                            {'node_names': lifecycle_nodes}])
        ]
    )

    ld = LaunchDescription()
    ld.add_action(declare_map_topic_name)
    ld.add_action(declare_map_yaml)
    ld.add_action(declare_use_sim_time)
    ld.add_action(declare_params_file)
    ld.add_action(declare_namespace)

    ld.add_action(launch_node)

    return ld
