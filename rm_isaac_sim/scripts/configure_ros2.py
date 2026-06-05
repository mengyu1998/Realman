#!/usr/bin/env python3
"""
RM65 Isaac Sim ROS2 配置脚本

功能:
1. 查找场景中的机械臂对象
2. 配置 ROS2 关节状态发布
3. 同步真实机械臂与虚拟机械臂

使用方法:
在 Isaac Sim 的 Script Editor 中运行此脚本
"""

import omni.usd


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
            robot_prims.append(prim_path)
            print(f"  ✓ 找到: {prim_path}")

    if not robot_prims:
        print("  ✗ 未找到机械臂对象")
        print("\n请确保 USD 文件已正确加载")

    return robot_prims


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
                ros2_bridge.create_joint_state_publisher(
                    robot_prim_path=robot_path,
                    topic_name="/arm_left/isaac_joint_states",
                    publish_rate=100
                )
                print(f"✓ 已配置话题: /arm_left/isaac_joint_states")
            except Exception as e:
                print(f"✗ 配置失败: {e}")
                print("可能原因:")
                print("  1. 机械臂对象没有 Articulation 组件")
                print("  2. 机械臂对象路径不正确")
                print("  3. ROS2 Bridge 扩展未正确加载")

            # 如果有第二个机械臂
            if len(robot_prims) > 1:
                robot_path2 = robot_prims[1]
                print(f"\n配置第二个机械臂: {robot_path2}")
                try:
                    ros2_bridge.create_joint_state_publisher(
                        robot_prim_path=robot_path2,
                        topic_name="/arm_right/isaac_joint_states",
                        publish_rate=100
                    )
                    print(f"✓ 已配置话题: /arm_right/isaac_joint_states")
                except Exception as e:
                    print(f"✗ 配置失败: {e}")
        else:
            print("\n未找到机械臂对象")
            print("请手动选择机械臂对象")
            print("\n手动配置步骤:")
            print("1. 在 Stage 面板中选择机械臂对象")
            print("2. 在 Property 面板中点击 'Add Component'")
            print("3. 搜索并添加 'ROS2 Joint State Publisher'")
            print("4. 配置话题名称和发布频率")

    except ImportError:
        print("\n✗ 错误: 无法导入 ROS2 Bridge")
        print("请确保已启用 ROS2 Bridge 扩展")
        print("菜单: Extensions → 搜索 'ROS2 Bridge' → 启用")
    except Exception as e:
        print(f"\n✗ 错误: ROS2 Bridge 配置失败: {e}")


def main():
    """主函数"""
    print("=" * 60)
    print("RM65 Isaac Sim ROS2 配置")
    print("=" * 60)

    # 查找机械臂对象
    robot_prims = find_robot_prims()

    # 配置 ROS2 Bridge
    configure_ros2_bridge(robot_prims)

    # 打印完成信息
    print("\n" + "=" * 60)
    print("配置完成!")
    print("=" * 60)
    print("\n下一步:")
    print("1. 在另一个终端中验证连接:")
    print("   source /home/realman/ros2_ws/install/setup.bash")
    print("   ros2 topic list")
    print("   ros2 topic echo /arm_left/isaac_joint_states")
    print("\n2. 如果配置失败，请手动配置 ROS2 Bridge")
    print("=" * 60)


if __name__ == '__main__':
    main()
