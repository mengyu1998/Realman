#!/usr/bin/env python3
"""
检查 USD 文件中的节点配置

功能:
1. 检查 USD 文件中的 ROS2 相关节点
2. 检查机械臂对象
3. 检查关节配置

使用方法:
在 Isaac Sim 的 Script Editor 中运行此脚本
"""

import omni.usd


def check_usd_structure():
    """检查 USD 文件结构"""
    print("\n" + "=" * 60)
    print("检查 USD 文件结构")
    print("=" * 60)

    stage = omni.usd.get_context().get_stage()

    # 统计节点数量
    prim_count = 0
    robot_prims = []
    ros2_nodes = []
    joint_prims = []

    for prim in stage.Traverse():
        prim_path = str(prim.GetPath())
        prim_count += 1

        # 查找机械臂对象
        if any(keyword in prim_path.lower() for keyword in ["robot", "arm", "rm_65", "manipulator"]):
            robot_prims.append(prim_path)

        # 查找 ROS2 相关节点
        if "ros2" in prim_path.lower() or "graph" in prim_path.lower():
            ros2_nodes.append(prim_path)

        # 查找关节
        if "joint" in prim_path.lower():
            joint_prims.append(prim_path)

    print(f"\n节点总数: {prim_count}")
    print(f"机械臂对象: {len(robot_prims)}")
    print(f"ROS2 相关节点: {len(ros2_nodes)}")
    print(f"关节对象: {len(joint_prims)}")

    # 显示机械臂对象
    if robot_prims:
        print("\n机械臂对象:")
        for prim in robot_prims:
            print(f"  ✓ {prim}")
    else:
        print("\n✗ 未找到机械臂对象")

    # 显示 ROS2 相关节点
    if ros2_nodes:
        print("\nROS2 相关节点:")
        for prim in ros2_nodes:
            print(f"  ✓ {prim}")
    else:
        print("\n✗ 未找到 ROS2 相关节点")

    # 显示关节对象
    if joint_prims:
        print("\n关节对象:")
        for prim in joint_prims:
            print(f"  ✓ {prim}")
    else:
        print("\n✗ 未找到关节对象")


def check_articulation():
    """检查 Articulation 配置"""
    print("\n" + "=" * 60)
    print("检查 Articulation 配置")
    print("=" * 60)

    stage = omni.usd.get_context().get_stage()

    articulation_prims = []
    for prim in stage.Traverse():
        prim_path = str(prim.GetPath())
        # 检查是否有 Articulation 组件
        if prim.HasAPI(Usd.ArticulationRootAPI):
            articulation_prims.append(prim_path)

    if articulation_prims:
        print("\n找到的 Articulation 对象:")
        for prim in articulation_prims:
            print(f"  ✓ {prim}")
    else:
        print("\n✗ 未找到 Articulation 对象")
        print("可能原因:")
        print("1. USD 文件中没有配置 Articulation")
        print("2. 机械臂对象没有设置为 Articulation Root")


def check_joint_names():
    """检查关节名称"""
    print("\n" + "=" * 60)
    print("检查关节名称")
    print("=" * 60)

    stage = omni.usd.get_context().get_stage()

    joint_names = []
    for prim in stage.Traverse():
        prim_path = str(prim.GetPath())
        prim_type = str(prim.GetTypeName())

        # 检查是否是关节
        if "joint" in prim_type.lower() or "revolute" in prim_type.lower() or "prismatic" in prim_type.lower():
            joint_name = prim_path.split("/")[-1]
            joint_names.append(joint_name)

    if joint_names:
        print("\n找到的关节:")
        for name in joint_names:
            print(f"  ✓ {name}")
    else:
        print("\n✗ 未找到关节")


def check_ros2_bridge_config():
    """检查 ROS2 Bridge 配置"""
    print("\n" + "=" * 60)
    print("检查 ROS2 Bridge 配置")
    print("=" * 60)

    try:
        from omni.isaac.ros2_bridge import Ros2Bridge
        print("\n✓ ROS2 Bridge 模块可用")

        # 尝试创建 ROS2 Bridge 实例
        ros2_bridge = Ros2Bridge()
        print("✓ ROS2 Bridge 实例创建成功")

        return True

    except ImportError as e:
        print(f"\n✗ ROS2 Bridge 模块不可用: {e}")
        print("请确保已启用 ROS2 Bridge 扩展")
        return False

    except Exception as e:
        print(f"\n✗ ROS2 Bridge 创建失败: {e}")
        return False


def main():
    """主函数"""
    print("=" * 60)
    print("RM65 Isaac Sim USD 文件检查")
    print("=" * 60)

    # 检查 USD 文件结构
    check_usd_structure()

    # 检查 Articulation 配置
    check_articulation()

    # 检查关节名称
    check_joint_names()

    # 检查 ROS2 Bridge 配置
    ros2_available = check_ros2_bridge_config()

    # 总结
    print("\n" + "=" * 60)
    print("检查总结")
    print("=" * 60)

    if ros2_available:
        print("\n✓ ROS2 Bridge 可用")
        print("  可以配置 ROS2 连接")
    else:
        print("\n✗ ROS2 Bridge 不可用")
        print("  请启用 ROS2 Bridge 扩展")

    print("\n下一步:")
    print("1. 如果未找到机械臂对象，请检查 USD 文件")
    print("2. 如果未找到 Articulation 对象，请配置 Articulation")
    print("3. 如果 ROS2 Bridge 不可用，请启用扩展")
    print("=" * 60)


if __name__ == '__main__':
    main()
