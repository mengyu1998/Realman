#!/bin/bash
# RM65 双臂连接脚本
# 连接真实机械臂与 Isaac Sim 虚拟机械臂

set -e

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}"
    echo "============================================"
    echo "$1"
    echo "============================================"
    echo -e "${NC}"
}

# 检查环境
check_environment() {
    print_header "检查环境"

    # 获取脚本目录
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    PACKAGE_DIR="$(dirname "$SCRIPT_DIR")"

    # 检查 USD 文件
    USD_FILE="$PACKAGE_DIR/rm_65_two_1_isaac.usd"
    if [ ! -f "$USD_FILE" ]; then
        print_error "USD 文件不存在: $USD_FILE"
        exit 1
    fi
    print_info "✓ USD 文件: $USD_FILE"

    # 检查 Isaac Sim
    ISAAC_SIM_PATH=${ISAAC_SIM_PATH:-/home/realman/isaacsim}
    if [ ! -d "$ISAAC_SIM_PATH" ]; then
        print_error "Isaac Sim 路径不存在: $ISAAC_SIM_PATH"
        exit 1
    fi
    print_info "✓ Isaac Sim 路径: $ISAAC_SIM_PATH"

    # 检查 isaac-sim.sh
    ISAAC_SIM_SCRIPT="$ISAAC_SIM_PATH/_build/linux-x86_64/release/isaac-sim.sh"
    if [ ! -f "$ISAAC_SIM_SCRIPT" ]; then
        print_error "无法找到 Isaac Sim 启动脚本: $ISAAC_SIM_SCRIPT"
        exit 1
    fi
    print_info "✓ Isaac Sim 启动脚本: $ISAAC_SIM_SCRIPT"

    # 检查 ROS2 环境
    if [ -z "$ROS_DISTRO" ]; then
        print_warn "未检测到 ROS2 环境"
        print_info "正在加载 ROS2 环境..."
        source /opt/ros/humble/setup.bash
    fi
    print_info "✓ ROS2 发行版: $ROS_DISTRO"

    # 加载工作空间
    print_info "加载工作空间环境..."
    source /home/realman/ros2_ws/install/setup.bash
}

# 显示操作步骤
show_steps() {
    print_header "连接步骤"

    print_info "请按照以下步骤操作:"
    print_info ""
    print_info "步骤 1: 启动 ROS2 系统（终端 1）"
    print_info "  source /opt/ros/humble/setup.bash"
    print_info "  source /home/realman/ros2_ws/install/setup.bash"
    print_info "  ros2 launch rm_isaac_sim dual_arm_isaac.launch.py"
    print_info ""
    print_info "步骤 2: 启动 Isaac Sim（终端 2）"
    print_info "  ./scripts/start_isaac.sh"
    print_info ""
    print_info "步骤 3: 在 Isaac Sim 中加载 USD 文件"
    print_info "  File → Open → $USD_FILE"
    print_info ""
    print_info "步骤 4: 启用 ROS2 Bridge 扩展"
    print_info "  Extensions → Extension Manager → 搜索 'ROS2 Bridge' → 启用"
    print_info ""
    print_info "步骤 5: 配置 ROS2 连接"
    print_info "  在 Script Editor 中运行: scripts/configure_ros2.py"
    print_info ""
    print_info "步骤 6: 验证连接（终端 3）"
    print_info "  source /home/realman/ros2_ws/install/setup.bash"
    print_info "  ros2 topic list"
    print_info "  ros2 topic echo /arm_left/isaac_joint_states"
    print_info ""
    print_info "============================================"
    print_info ""
}

# 主函数
main() {
    print_header "RM65 双臂 Isaac Sim 连接"

    # 检查环境
    check_environment

    # 显示操作步骤
    show_steps

    print_info "按 Enter 退出..."
    read -r
}

# 运行主函数
main "$@"
