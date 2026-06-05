#!/usr/bin/env python3
"""
RM65 Isaac Sim USD 文件配置脚本

功能:
1. 查找机械臂对象
2. 添加 Articulation Root
3. 配置 ROS2 关节状态发布
4. 配置 ROS2 关节状态订阅
5. 保存 USD 文件

使用方法:
在 Isaac Sim 的 Script Editor 中运行此脚本
"""

import omni.usd
from pxr import Usd, UsdPhysics, Sdf


def find_robot_prims():
    """查找场景中的机械臂对象"""
    stage = omni.usd.get_context().get_stage()
    robot_prims = []

    print("\n" + "=" * 60)
    print("查找机械臂对象...")
    print("=" * 60)

    for prim in stage.Traverse():
        prim_path = str(prim.GetPath())
        # 查找可能的机械臂对象
        if any(keyword in prim_path.lower() for keyword in ["robot", "arm", "rm_65", "manipulator"]):
            # 检查是否是根对象（通常在 /World 下）
            if prim_path.count("/") <= 3:  # 例如 /World/rm_65_left
                robot_prims.append(prim_path)
                print(f"  ✓ 找到: {prim_path}")

    if not robot_prims:
        print("  ✗ 未找到机械臂对象")
        print("\n请确保 USD 文件已正确加载")

    return robot_prims


def add_articulation_root(prim_path):
    """为机械臂添加 Articulation Root"""
    print(f"\n为 {prim_path} 添加 Articulation Root...")

    stage = omni.usd.get_context().get_stage()
    prim = stage.GetPrimAtPath(prim_path)

    if not prim:
        print(f"  ✗ 未找到对象: {prim_path}")
        return False

    try:
        # 添加 Articulation Root API
        UsdPhysics.ArticulationRootAPI.Apply(prim)
        print(f"  ✓ 已添加 Articulation Root")
        return True
    except Exception as e:
        print(f"  ✗ 添加失败: {e}")
        return False


def setup_ros2_publisher(prim_path, topic_name):
    """设置 ROS2 关节状态发布"""
    print(f"\n为 {prim_path} 配置 ROS2 发布...")

    stage = omni.usd.get_context().get_stage()
    prim = stage.GetPrimAtPath(prim_path)

    if not prim:
        print(f"  ✗ 未找到对象: {prim_path}")
        return False

    try:
        # 这里需要使用 Isaac Sim 的 ROS2 Bridge API
        # 实际配置会在 Script Editor 中使用 Ros2Bridge 类
        print(f"  ✓ 准备配置 ROS2 发布: {topic_name}")
        return True
    except Exception as e:
        print(f"  ✗ 配置失败: {e}")
        return False


def setup_ros2_subscriber(prim_path, topic_name):
    """设置 ROS2 关节状态订阅"""
    print(f"\n为 {prim_path} 配置 ROS2 订阅...")

    stage = omni.usd.get_context().get_stage()
    prim = stage.GetPrimAtPath(prim_path)

    if not prim:
        print(f"  ✗ 未找到对象: {prim_path}")
        return False

    try:
        # 这里需要使用 Isaac Sim 的 ROS2 Bridge API
        # 实际配置会在 Script Editor 中使用 Ros2Bridge 类
        print(f"  ✓ 准备配置 ROS2 订阅: {topic_name}")
        return True
    except Exception as e:
        print(f"  ✗ 配置失败: {e}")
        return False


def configure_ros2_bridge(robot_prims):
    """配置 ROS2 Bridge"""
    print("\n" + "=" * 60)
    print("配置 ROS2 Bridge...")
    print("=" * 60)

    try:
        from omni.isaac.ros2_bridge import Ros2Bridge

        # 创建 ROS2 Bridge
        ros2_bridge = Ros2Bridge()
        print("\n✓ ROS2 Bridge 初始化成功")

        # 配置关节状态发布
        if robot_prims:
            # 配置第一个机械臂
            robot_path = robot_prims[0]
            print(f"\n配置机械臂: {robot_path}")

            try:
                # 添加 Articulation Root
                add_articulation_root(robot_path)

                # 配置 ROS2 发布
                ros2_bridge.create_joint_state_publisher(
                    robot_prim_path=robot_path,
                    topic_name="/arm_left/isaac_joint_states",
                    publish_rate=100
                )
                print(f"✓ 已配置发布: /arm_left/isaac_joint_states")

                # 配置 ROS2 订阅
                ros2_bridge.create_joint_state_subscriber(
                    robot_prim_path=robot_path,
                    topic_name="/arm_left/joint_states",
                    callback=lambda msg: None  # 回调函数
                )
                print(f"✓ 已配置订阅: /arm_left/joint_states")

            except Exception as e:
                print(f"✗ 配置失败: {e}")

            # 如果有第二个机械臂
            if len(robot_prims) > 1:
                robot_path2 = robot_prims[1]
                print(f"\n配置第二个机械臂: {robot_path2}")

                try:
                    # 添加 Articulation Root
                    add_articulation_root(robot_path2)

                    # 配置 ROS2 发布
                    ros2_bridge.create_joint_state_publisher(
                        robot_prim_path=robot_path2,
                        topic_name="/arm_right/isaac_joint_states",
                        publish_rate=100
                    )
                    print(f"✓ 已配置发布: /arm_right/isaac_joint_states")

                    # 配置 ROS2 订阅
                    ros2_bridge.create_joint_state_subscriber(
                        robot_prim_path=robot_path2,
                        topic_name="/arm_right/joint_states",
                        callback=lambda msg: None  # 回调函数
                    )
                    print(f"✓ 已配置订阅: /arm_right/joint_states")

                except Exception as e:
                    print(f"✗ 配置失败: {e}")
        else:
            print("\n未找到机械臂对象")

    except ImportError:
        print("\n✗ 错误: 无法导入 ROS2 Bridge")
        print("请确保已启用 ROS2 Bridge 扩展")
        return False

    except Exception as e:
        print(f"\n✗ 错误: ROS2 Bridge 配置失败: {e}")
        return False

    return True


def save_usd():
    """保存 USD 文件"""
    print("\n" + "=" * 60)
    print("保存 USD 文件...")
    print("=" * 60)

    try:
        stage = omni.usd.get_context().get_stage()

        # 保存到原文件
        usd_file = "/home/realman/ros2_ws/src/ros2_rm_robot/rm_isaac_sim/rm_65_two_1_isaac.usd"
        stage.Export(usd_file)
        print(f"\n✓ USD 文件已保存: {usd_file}")

        return True

    except Exception as e:
        print(f"\n✗ 保存失败: {e}")
        return False


def main():
    """主函数"""
    print("=" * 60)
    print("RM65 Isaac Sim USD 文件配置")
    print("=" * 60)

    # 查找机械臂对象
    robot_prims = find_robot_prims()

    if not robot_prims:
        print("\n未找到机械臂对象，无法继续配置")
        return

    # 配置 ROS2 Bridge
    success = configure_ros2_bridge(robot_prims)

    if success:
        # 保存 USD 文件
        save_usd()

        print("\n" + "=" * 60)
        print("配置完成!")
        print("=" * 60)
        print("\n下一步:")
        print("1. 重启 Isaac Sim")
        print("2. 重新加载 USD 文件")
        print("3. 启用 ROS2 Bridge 扩展")
        print("4. 验证连接:")
        print("   ros2 topic list")
        print("   ros2 topic echo /arm_left/isaac_joint_states")
        print("=" * 60)
    else:
        print("\n配置失败，请检查错误信息")


if __name__ == '__main__':
    main()
