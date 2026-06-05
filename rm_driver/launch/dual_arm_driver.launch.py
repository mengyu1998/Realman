import launch
import os
import yaml
import launch_ros
from launch import LaunchDescription
from launch_ros.actions import Node, PushRosNamespace
from launch.actions import GroupAction, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    rm_driver_pkg = get_package_share_directory('rm_driver')

    return LaunchDescription([

        # 左臂
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(rm_driver_pkg, 'launch', 'rm_65_left_driver.launch.py')
            )
        ),

        # 右臂
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(rm_driver_pkg, 'launch', 'rm_65_right_driver.launch.py')
            )
        )

    ])
