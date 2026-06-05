#!/bin/bash
# 启动 Isaac Sim 并加载 USD 文件

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

# 主函数
main() {
    print_header "启动 Isaac Sim"

    # 获取 USD 文件路径
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    PACKAGE_DIR="$(dirname "$SCRIPT_DIR")"
    USD_FILE="$PACKAGE_DIR/rm_65_two_1_isaac.usd"

    # 检查 USD 文件
    if [ ! -f "$USD_FILE" ]; then
        print_error "USD 文件不存在: $USD_FILE"
        exit 1
    fi
    print_info "✓ USD 文件: $USD_FILE"

    # 设置 Isaac Sim 路径
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

    # 启动 Isaac Sim
    print_info "启动 Isaac Sim..."
    print_info ""
    print_info "操作步骤:"
    print_info "1. 等待 Isaac Sim 启动"
    print_info "2. 在 Isaac Sim 中加载 USD 文件:"
    print_info "   File → Open → $USD_FILE"
    print_info "3. 启用 ROS2 Bridge 扩展"
    print_info "4. 配置 ROS2 连接"
    print_info ""
    print_info "============================================"
    print_info ""

    # 启动 Isaac Sim
    "$ISAAC_SIM_SCRIPT"
}

# 运行主函数
main "$@"
