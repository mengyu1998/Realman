# RM65 双臂 Isaac Sim 集成功能包

## 📋 功能包概述

本功能包实现了睿尔曼 RM65 双臂系统与 NVIDIA Isaac Sim 的集成，允许在虚拟环境中同步和控制真实机械臂。

## 📁 功能包结构

```
rm_isaac_sim/
├── rm_65_two_1_isaac.usd              # 主要 USD 场景文件
├── rm_65_isaac.usd                    # 单臂 USD 场景文件
├── rm_65_isaac_two.usd                # 双臂 USD 场景文件
├── package.xml                        # ROS2 功能包描述
├── CMakeLists.txt                     # CMake 配置
├── README.md                          # 本文档
├── configuration/                     # USD 配置文件目录
│   ├── rm_65_isaac_two_base.usd       # 基础配置
│   ├── rm_65_isaac_two_physics.usd    # 物理配置
│   ├── rm_65_isaac_two_robot.usd      # 机器人配置
│   └── rm_65_isaac_two_sensor.usd     # 传感器配置
├── config/                            # 配置文件目录
├── launch/                            # Launch 文件目录
└── scripts/                           # 脚本文件目录
    ├── isaac_ros_bridge.py            # ROS2 桥接节点
    ├── configure_ros2.py              # ROS2 配置脚本
    ├── check_usd.py                   # USD 文件检查脚本
    ├── setup_usd.py                   # USD 文件配置脚本
    ├── start_isaac.sh                 # 启动 Isaac Sim 脚本
    └── connect.sh                     # 连接脚本
```

## 🚀 快速开始

### 步骤 1: 编译功能包

```bash
cd /home/realman/ros2_ws
colcon build --packages-select rm_isaac_sim
source install/setup.bash
```

### 步骤 2: 启动 ROS2 系统（终端 1）

```bash
source /opt/ros/humble/setup.bash
source /home/realman/ros2_ws/install/setup.bash
ros2 launch rm_driver dual_arm_driver.launch.py
```

**预期结果**: 终端显示 "waiting for connect"

### 步骤 3: 启动 Isaac Sim（终端 2）

```bash
cd /home/realman/ros2_ws/src/ros2_rm_robot/rm_isaac_sim
./scripts/start_isaac.sh
```

**预期结果**: Isaac Sim 启动

### 步骤 4: 在 Isaac Sim 中加载 USD 文件

1. 菜单: **File** → **Open**
2. 选择: `/home/realman/ros2_ws/src/ros2_rm_robot/rm_isaac_sim/rm_65_isaac_two.usd`
3. 点击 **Open**

**预期结果**: 双臂模型显示在场景中

### 步骤 5: 启用 ROS2 Bridge 扩展（不用，已经完成）

1. 菜单: **Extensions** → **Extension Manager**
2. 搜索: `ROS2 Bridge`
3. 启用扩展: `omni.isaac.ros2_bridge`

**预期结果**: 扩展启用成功

### 步骤 6: 配置 ROS2 连接(不用，已经在步骤四完成)

在 Isaac Sim 的 **Script Editor** 中运行：

```python
# 复制 scripts/configure_ros2.py 的内容到 Script Editor
# 或者直接运行以下代码:

import omni.usd

def find_robot_prims():
    stage = omni.usd.get_context().get_stage()
    robot_prims = []
    print("\n查找机械臂对象...")
    for prim in stage.Traverse():
        prim_path = str(prim.GetPath())
        if any(keyword in prim_path.lower() for keyword in ["robot", "arm", "rm_65", "manipulator"]):
            robot_prims.append(prim_path)
            print(f"  ✓ 找到: {prim_path}")
    return robot_prims

def configure_ros2_bridge(robot_prims):
    try:
        from omni.isaac.ros2_bridge import Ros2Bridge
        ros2_bridge = Ros2Bridge()
        print("\n✓ ROS2 Bridge 初始化成功")

        if robot_prims:
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
    except ImportError:
        print("\n✗ 错误: 无法导入 ROS2 Bridge")
        print("请确保已启用 ROS2 Bridge 扩展")
    except Exception as e:
        print(f"\n✗ 错误: ROS2 Bridge 配置失败: {e}")

# 运行配置
robot_prims = find_robot_prims()
configure_ros2_bridge(robot_prims)
```

**预期结果**: 看到 "✓ 已配置话题" 消息

### 步骤 7: 验证连接（终端 3）

```bash
source /home/realman/ros2_ws/install/setup.bash
ros2 topic list
ros2 topic echo /arm_left/isaac_joint_states
ros2 topic echo /arm_right/isaac_joint_states
```

**预期结果**: 看到关节状态数据

## 📊 ROS2 话题说明

### 关节状态话题

| 话题名称 | 消息类型 | 说明 |
|----------|----------|------|
| `/arm_left/joint_states` | sensor_msgs/JointState | 真实左臂关节状态 |
| `/arm_right/joint_states` | sensor_msgs/JointState | 真实右臂关节状态 |
| `/arm_left/isaac_joint_states` | sensor_msgs/JointState | Isaac Sim 左臂关节状态 |
| `/arm_right/isaac_joint_states` | sensor_msgs/JointState | Isaac Sim 右臂关节状态 |

### 关节详细信息话题

| 话题名称 | 说明 |
|----------|------|
| `/arm_left/rm_driver/udp_joint_speed` | 左臂关节速度 |
| `/arm_left/rm_driver/udp_joint_current` | 左臂关节电流 |
| `/arm_left/rm_driver/udp_joint_temperature` | 左臂关节温度 |
| `/arm_left/rm_driver/udp_joint_voltage` | 左臂关节电压 |
| `/arm_left/rm_driver/udp_joint_error_code` | 左臂关节错误代码 |
| `/arm_left/rm_driver/udp_joint_en_flag` | 左臂关节使能标志 |
| `/arm_left/rm_driver/udp_joint_pose_euler` | 左臂关节位姿（欧拉角） |

## 🔧 脚本说明

### isaac_ros_bridge.py

ROS2 桥接节点，用于连接真实机械臂和 Isaac Sim。

**功能**:
- 订阅真实机械臂的关节状态
- 将关节状态发布到 Isaac Sim
- 同步虚拟机械臂与真实机械臂的状态

**使用方法**:
```bash
ros2 run rm_isaac_sim isaac_ros_bridge
```

### configure_ros2.py

ROS2 配置脚本，用于在 Isaac Sim 中配置 ROS2 连接。

**功能**:
- 查找场景中的机械臂对象
- 配置 ROS2 关节状态发布
- 同步真实机械臂与虚拟机械臂

**使用方法**:
在 Isaac Sim 的 Script Editor 中运行此脚本

### check_usd.py

USD 文件检查脚本，用于检查 USD 文件中的节点配置。

**功能**:
- 检查 USD 文件中的 ROS2 相关节点
- 检查机械臂对象
- 检查关节配置

**使用方法**:
在 Isaac Sim 的 Script Editor 中运行此脚本

### setup_usd.py

USD 文件配置脚本，用于配置 USD 文件中的 ROS2 组件。

**功能**:
- 查找机械臂对象
- 添加 Articulation Root
- 配置 ROS2 关节状态发布
- 配置 ROS2 关节状态订阅
- 保存 USD 文件

**使用方法**:
在 Isaac Sim 的 Script Editor 中运行此脚本

### start_isaac.sh

启动 Isaac Sim 脚本。

**功能**:
- 检查 USD 文件
- 检查 Isaac Sim 路径
- 启动 Isaac Sim

**使用方法**:
```bash
./scripts/start_isaac.sh
```

### connect.sh

连接脚本，用于引导用户完成连接过程。

**功能**:
- 检查环境
- 显示操作步骤
- 引导用户完成连接

**使用方法**:
```bash
./scripts/connect.sh
```

## 🔧 常见问题

### 问题 1: "无法导入 ROS2 Bridge"

**解决方案**:
1. 确保已启用 ROS2 Bridge 扩展
2. 重启 Isaac Sim
3. 检查 Isaac Sim 版本

### 问题 2: "未找到机械臂对象"

**解决方案**:
1. 确保 USD 文件已正确加载
2. 在 Stage 面板中查看对象层次结构
3. 手动查找机械臂对象路径

### 问题 3: "ROS2 话题未出现"

**解决方案**:
1. 确保 ROS2 系统已启动
2. 检查 ROS2 环境是否正确加载
3. 重启 ROS2 系统

### 问题 4: "配置文件未找到"

**解决方案**:
1. 检查配置文件路径
2. 确保配置文件存在
3. 重新编译功能包

## 📊 验证配置

### 检查 ROS2 话题

```bash
# 列出所有话题
ros2 topic list

# 应该看到:
# /arm_left/joint_states
# /arm_right/joint_states
# /arm_left/isaac_joint_states
# /arm_right/isaac_joint_states
```

### 检查话题数据

```bash
# 查看左臂关节状态
ros2 topic echo /arm_left/joint_states

# 查看右臂关节状态
ros2 topic echo /arm_right/joint_states
```

### 检查话题频率

```bash
# 查看话题发布频率
ros2 topic hz /arm_left/joint_states
ros2 topic hz /arm_right/joint_states
```

## 🎉 连接成功后

当连接成功后，你应该能够：

✅ 在 Isaac Sim 中看到虚拟 RM65 双臂
✅ 虚拟机械臂跟随真实机械臂运动
✅ 通过 Isaac Sim 控制真实机械臂
✅ 使用相机进行视觉反馈
✅ 进行双臂协同操作

## 📚 相关文档

| 文档 | 用途 |
|------|------|
| [README.md](README.md) | **本文档** - 功能包完整说明 |
| [scripts/connect.sh](scripts/connect.sh) | 连接脚本 |
| [scripts/configure_ros2.py](scripts/configure_ros2.py) | ROS2 配置脚本 |
| [scripts/check_usd.py](scripts/check_usd.py) | USD 文件检查脚本 |
| [scripts/setup_usd.py](scripts/setup_usd.py) | USD 文件配置脚本 |

## 🆘 获取帮助

- **查看日志**: Isaac Sim Console
- **检查节点**: `ros2 node list`
- **查看话题**: `ros2 topic list`
- **运行连接脚本**: `./scripts/connect.sh`

## 📝 更新日志

### v1.0.0 (2026-06-03)
- 初始版本
- 支持 RM65 双臂系统
- 实现 ROS2 桥接功能
- 提供完整的文档和示例
