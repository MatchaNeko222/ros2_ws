# ROS2 学习文档：在 Python 类中使用参数（已实战验证）

## 1. 学习目标

- 在 Python 节点类中创建参数并读取参数。
- 在运行时动态修改参数，并让节点行为立即变化。
- 使用自定义消息进行发布。
- 使用 launch 文件一键启动并注入参数。

---

## 2. 已完成内容

### 2.1 参数节点

已实现一个参数化发布节点，节点会发布自定义消息 PersonInfo，并通过参数控制发布行为。

节点文件：
- src/my_test_pkg/my_test_pkg/person_info_param_publisher.py

这个节点包含：
- 参数声明（declare_parameter）
- 参数读取（get_parameter）
- 动态参数回调（add_on_set_parameters_callback）
- 参数校验（周期必须大于 0，年龄范围 0 到 120）
- 参数更新后重建定时器，让新周期立即生效

### 2.2 包配置

已补齐依赖和入口点。

配置文件：
- src/my_test_pkg/package.xml
- src/my_test_pkg/setup.py

关键点：
- 新增 rcl_interfaces 依赖（参数回调结果类型需要）
- 新增 launch、launch_ros 依赖
- 增加 console_scripts 入口：person_info_param_publisher
- 安装 launch 文件到 share 目录

### 2.3 启动文件

已新增 launch 文件，支持一键启动并传入参数。

启动文件：
- src/my_test_pkg/launch/person_info_param.launch.py

支持启动参数：
- topic_name
- publish_period
- default_name
- default_age

---

## 3. 运行步骤

### 3.1 构建

cd /home/luckiop/IDEA_learn_ws/ros2_ws/MY_NEW_WS
source /opt/ros/humble/setup.bash
colcon build --packages-select my_test_pkg

### 3.2 运行（单节点方式）

source /home/luckiop/IDEA_learn_ws/ros2_ws/MY_NEW_WS/install/setup.bash
ros2 run my_test_pkg person_info_param_publisher

### 3.3 运行（launch 方式）

source /home/luckiop/IDEA_learn_ws/ros2_ws/MY_NEW_WS/install/setup.bash
ros2 launch my_test_pkg person_info_param.launch.py

### 3.4 launch 时覆盖参数

ros2 launch my_test_pkg person_info_param.launch.py publish_period:=3.0 default_name:=Demo default_age:=26

---

## 4. 动态调参（运行中）

### 4.1 查看参数

ros2 param get /person_info_param_publisher publish_period

### 4.2 修改参数

ros2 param set /person_info_param_publisher publish_period 10.0
ros2 param set /person_info_param_publisher default_name Alice
ros2 param set /person_info_param_publisher default_age 28

---

## 5. 验证结论

本次已实测通过：

- publish_period 从 10.0 调为 1.0 后，日志变为接近每秒一条。
- 再调回 10.0 后，日志恢复为约每 10 秒一条。
- 说明动态参数回调生效，且参数真实驱动了类行为。

---

## 6. 常见问题

### 6.1 为什么出现退出码 254

多数是手动 Ctrl+C 中断节点引起，不是代码错误。
1
### 6.2 为什么改了 setup.py 还找不到新命令

通常是没有重新 build，或运行前没有 source install/setup.bash。

### 6.3 参数改了但节点行为没变

常见原因：只声明了参数，但业务逻辑没有使用更新后的成员变量。

---

## 7. 学习收获

你已经完成了一个完整闭环：

- 自定义消息定义
- Python 类参数化节点开发
- 运行时动态调参
- launch 启动与参数注入

这套流程已经达到项目实战基础能力，可以继续扩展到服务、动作、多节点协同和 YAML 参数管理。
