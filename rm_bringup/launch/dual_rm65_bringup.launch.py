import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, GroupAction, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node, PushRosNamespace


def generate_launch_description():
    # 获取各包的路径
    rm_driver_pkg = get_package_share_directory('rm_driver')
    rm_description_pkg = get_package_share_directory('rm_description')
    rm_control_pkg = get_package_share_directory('rm_control')
    rm_moveit_config_pkg = get_package_share_directory('rm_65_config')

    # 左机械臂的启动组
    left_arm_group = GroupAction(
        actions=[
            PushRosNamespace('arm_left'),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(os.path.join(rm_driver_pkg, 'launch', 'rm_65_driver.launch.py'))
            ),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(os.path.join(rm_description_pkg, 'launch', 'rm_65_display.launch.py'))
            ),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(os.path.join(rm_control_pkg, 'launch', 'rm_65_control.launch.py'))
            ),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(os.path.join(rm_moveit_config_pkg, 'launch', 'real_moveit_demo.launch.py'))
            )
        ]
    )

    # 右机械臂的启动组
    right_arm_group = GroupAction(
        actions=[
            PushRosNamespace('arm_right'),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(os.path.join(rm_driver_pkg, 'launch', 'rm_65_driver.launch.py'))
            ),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(os.path.join(rm_description_pkg, 'launch', 'rm_65_display.launch.py'))
            ),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(os.path.join(rm_control_pkg, 'launch', 'rm_65_control.launch.py'))
            ),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(os.path.join(rm_moveit_config_pkg, 'launch', 'real_moveit_demo.launch.py'))
            )
        ]
    )

    return LaunchDescription([
        left_arm_group,
        right_arm_group,
    ])
