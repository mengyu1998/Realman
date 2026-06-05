cmake_minimum_required(VERSION 3.10)
project(rm_isaac_sim)

find_package(ament_cmake REQUIRED)

# 安装 Launch 文件
install(DIRECTORY
  launch
  DESTINATION share/${PROJECT_NAME}
)

# 安装脚本文件到 lib 目录
install(PROGRAMS
  scripts/isaac_ros_bridge.py
  scripts/configure_ros2.py
  DESTINATION lib/${PROJECT_NAME}
)

# 安装其他脚本文件到 share 目录
install(DIRECTORY
  scripts
  DESTINATION share/${PROJECT_NAME}
  FILE_PERMISSIONS OWNER_READ OWNER_WRITE OWNER_EXECUTE GROUP_READ GROUP_EXECUTE WORLD_READ WORLD_EXECUTE
  PATTERN "isaac_ros_bridge.py" EXCLUDE
  PATTERN "configure_ros2.py" EXCLUDE
)

# 安装配置文件
install(DIRECTORY
  config
  DESTINATION share/${PROJECT_NAME}
)

# 安装 USD 文件
install(FILES
  rm_65_two_1_isaac.usd
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
