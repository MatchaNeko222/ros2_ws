# 已知问题与现状

## 进展与现状

- 任务节点可启动并持续发布 setpoint。
- 起飞阶段可达目标高度（z≈3.0）。
- 前进阶段在部分环境中不执行：setpoint 有变化，但位置不动。

## 已定位问题

- 主要问题是位置不动：setpoint 有变化，但 `local_position/pose` 的 x/y/z 不动。
- 当前未稳定复现明显 failsafe 文本提示。
- 如果 MAVROS 未启动或环境未 source，`/mavros/param/set` 会一直等待服务。
- bringup 中 `simple_mission_node` 可能与任务节点冲突，已从 `demo_drone_bringup` 的 `gazebo_demo.launch.py` 中移除。

## 建议排查项

- `/mavros/state` 是否持续 `mode: GUIDED` 且 `armed: true`。（已解决）
- `/mavros/statustext/recv` 是否持续出现拒绝或限制提示。
- 确认只启动一套 SITL + MAVROS，且 `ROS_DOMAIN_ID` 一致。
