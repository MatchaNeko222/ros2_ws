# demo_takeoff_flight_land

一个小型 ROS 2 包，基于 MAVROS 在 Gazebo 中控制飞机起飞、直线前进 3 米，然后降落。

## 前置条件

- ROS 2 Humble
- 已安装 MAVROS 和 geographiclib 数据集
- 已按你的 demo_in_gazebo 流程启动 SITL + Gazebo

## 编译

```bash
cd /home/luckiop/IDEA_learn_ws/ros2_ws/demo_起飞飞行降落
source /opt/ros/humble/setup.bash
colcon build --packages-select demo_takeoff_flight_land
source install/setup.bash
```

## 运行

终端 1（SITL + Gazebo）：

```bash
cd /home/luckiop/IDEA_development_ws/demo_in_gazebo
bash scripts/start_sitl_gazebo.sh
```

终端 2（bringup + MAVROS）：

```bash
cd /home/luckiop/IDEA_development_ws/demo_in_gazebo
source /opt/ros/humble/setup.bash
source install/setup.bash
export ROS_DOMAIN_ID=0
ros2 launch demo_drone_bringup gazebo_demo.launch.py auto_takeoff:=false
```

终端 3（任务节点）：

```bash
cd /home/luckiop/IDEA_learn_ws/ros2_ws/demo_起飞飞行降落
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 launch demo_takeoff_flight_land mission.launch.py
```

## 验证流程（纯终端）

终端 4（连接与模式状态）：

```bash
source /opt/ros/humble/setup.bash
source /home/luckiop/IDEA_development_ws/demo_in_gazebo/install/setup.bash
ros2 topic echo /mavros/state
```

关注字段：

- `connected: true`
- `mode: GUIDED`
- `armed: true`

终端 5（飞行轨迹）：

```bash
source /opt/ros/humble/setup.bash
source /home/luckiop/IDEA_development_ws/demo_in_gazebo/install/setup.bash
ros2 topic echo /mavros/local_position/pose
```

判定要点：

- `pose.position.z` 先上升到约 3.0
- `pose.position.x` 增加约 3.0
- 最后 `pose.position.z` 下降到接近 0

终端 6（可选：确认 setpoint 频率）：

```bash
source /opt/ros/humble/setup.bash
source /home/luckiop/IDEA_development_ws/demo_in_gazebo/install/setup.bash
ros2 topic hz /mavros/setpoint_position/local
```

如果频率为 0，说明任务节点没有在持续发送 setpoint。

## 故障排查提示

- 如果 `/mavros/state.connected` 一直是 false，确认只启动了一套 SITL 和一套 MAVROS。
- 如果系统缺少 MAVROS，请安装 `ros-humble-mavros` 和 `ros-humble-mavros-extras`，并运行 geographiclib 安装脚本。
- 如果 MAVROS 启动早期崩溃，请让你的 MAVROS launch 文件对齐上游 APM 的启动方式。
- 如果 SITL 报 JSON 传感器消息缺失，请修正 SITL 启动脚本里的 Gazebo 插件路径。
