import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    package_name='adamo'
    gz_params_file = os.path.join(get_package_share_directory(package_name),'config','gz_params.yaml')

    rsp = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','rsp.launch.py'
                )]), launch_arguments={'use_sim_time': 'true', 'use_ros2_control': 'true'}.items()
    )

    # include the gazebo launch file (in the gazebo_ros package)
    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py'
                )]),
                launch_arguments={'extra_gazebo_args': '--ros-args --params-file ' + gz_params_file}.items()
    )

    # run spawner node from the gazebo_ros package
    # the entity name doesn't really matter if there's only have a single robot
    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-topic', 'robot_description',
                                   '-entity', 'bot'],
                        output='screen'
    )
    
    diff_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["diff_controller"],
    )

    joint_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_broadcaster"],
    )

    # launch simulation
    return LaunchDescription([
        rsp,
        gazebo,
        spawn_entity,
        diff_controller_spawner,
        joint_broadcaster_spawner
    ])