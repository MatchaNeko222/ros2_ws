# demo_in_gazebo 事故记录

只保留已经在本项目里验证过的启动结论、复现命令和修复结果。

## 标准关闭

```bash
pkill -f "sim_vehicle.py|arducopter|gz sim|mavros_node|ros2 launch demo_drone_bringup" || true
```

## 标准启动

终端 1：

```bash
cd /home/luckiop/IDEA_development_ws/demo_in_gazebo
bash scripts/start_sitl_gazebo.sh
```

终端 2：

```bash
cd /home/luckiop/IDEA_development_ws/demo_in_gazebo
source /opt/ros/humble/setup.bash
source install/setup.bash
export ROS_DOMAIN_ID=0
ros2 launch demo_drone_bringup gazebo_demo.launch.py auto_takeoff:=true
```

## 成功判定

```bash
ros2 node list
ros2 topic info -v /mavros/state
ros2 topic echo /mavros/state
```

能看到 `/mavros_router` 和 `/simple_mission_node`，并且 `/mavros/state.connected` 变成 `true`。

## Issue-001: MAVROS 未安装

复现：直接启动 bringup 时提示 `package 'mavros' not found`。

结论：系统缺少 MAVROS。

修复：

```bash
sudo apt update
sudo apt install -y ros-humble-mavros ros-humble-mavros-extras
sudo /opt/ros/humble/lib/mavros/install_geographiclib_datasets.sh
```

## Issue-002: `connected: false`

复现：`/mavros/state` 一直连不上 FCU。

结论：通常是启动链路不对、重复起了仿真，或 MAVROS 实例冲突。

处理：

```bash
pkill -f "sim_vehicle.py|arducopter|gz sim|mavros_node|ros2 launch demo_drone_bringup" || true
```

然后只保留一套仿真和一套 MAVROS，使用项目默认启动方式。

可忽略的 warning：

```text
your FCU don't support AUTOPILOT_VERSION, switched to default capabilities
```

## Issue-003: MAVROS 启动早期崩溃

复现：执行 `ros2 launch demo_drone_bringup gazebo_demo.launch.py` 后，`mavros_node` 在初始化阶段报 `create_subscription() called for existing topic name rt/mavros/mavros_node/status with incompatible type`，随后以 `invalid allocator` 退出。

结论：不是 SITL 链路本身的问题，而是本项目原先的 MAVROS 启动方式和 Humble 上游 APM launch 方式不一致。

修复：把 [src/demo_drone_bringup/launch/mavros.launch.py](src/demo_drone_bringup/launch/mavros.launch.py) 改成参考 MAVROS 自带的 APM launch 方式，去掉显式节点名，先加载 MAVROS 自带的 `apm_pluginlists.yaml` 和 `apm_config.yaml`，再叠加本项目的 `mavros_config.yaml`。

验证：重新 build 后再次启动，`mavros_node` 正常拉起，`simple_mission_node` 能连到 `/mavros/state`，不再复现崩溃。

## Issue-004: Gazebo 已起但 SITL 一直等 JSON

复现：只执行终端 1 的 `bash scripts/start_sitl_gazebo.sh`，Gazebo 里能看到飞机，但 `sim_vehicle.py` 一直输出 `No JSON sensor message received, resending servos`。

结论：SITL 本身已经启动，问题在 Gazebo 侧的 ArduPilot 插件/资源路径没有按本机实际布局正确加载，导致 JSON 传感器链路没有真正建立。

修复：把 [scripts/start_sitl_gazebo.sh](scripts/start_sitl_gazebo.sh) 改成同时兼容 `ardupilot_gazebo/install` 和 `ardupilot_gazebo/build` 两种布局，并同时导出 `GZ_SIM_SYSTEM_PLUGIN_PATH` 和 `GZ_SIM_PLUGIN_PATH`，减少插件找不到的概率。

验证：脚本先通过了 `bash -n` 语法检查；接下来需要重新跑终端 1，确认 Gazebo 端能正常加载 ArduPilot 插件，并且 SITL 不再持续报 JSON sensor message 缺失。

## 让飞机动起来

自动起飞：

```bash
ros2 launch demo_drone_bringup gazebo_demo.launch.py auto_takeoff:=true
```

手动发目标：

```bash
ros2 topic pub -r 10 /mavros/setpoint_position/local geometry_msgs/msg/PoseStamped "{header: {frame_id: map}, pose: {position: {x: 5.0, y: 0.0, z: 5.0}, orientation: {w: 1.0}}}"
```

手动解锁和切模式：

```bash
ros2 service call /mavros/set_mode mavros_msgs/srv/SetMode "{custom_mode: 'GUIDED'}"
ros2 service call /mavros/cmd/arming mavros_msgs/srv/CommandBool "{value: true}"
ros2 service call /mavros/cmd/takeoff mavros_msgs/srv/CommandTOL "{altitude: 5.0, latitude: 0.0, longitude: 0.0, min_pitch: 0.0, yaw: 0.0}"
```