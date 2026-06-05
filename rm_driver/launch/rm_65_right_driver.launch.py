import launch
import os
import yaml
import launch_ros
from launch import LaunchDescription
from launch_ros.actions import Node, PushRosNamespace
from launch.actions import GroupAction
from launch.substitutions import Command, LaunchConfiguration
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    arm_config = os.path.join(get_package_share_directory('rm_driver'),'config','rm_65_right_config.yaml')

    # 读取配置文件
    with open(arm_config,'r') as f:
        config = yaml.safe_load(f)

    # 提取参数
    params = config["rm_driver"]["ros__parameters"]

    return LaunchDescription([

        GroupAction([
            PushRosNamespace('arm_right'),
            Node(
                package= "rm_driver",
                executable= "rm_driver",
                name= "rm_driver",  # 明确指定节点名称
                parameters= [params],  # 直接传递参数字典
                output= 'screen'
            )
        ])

    ])
