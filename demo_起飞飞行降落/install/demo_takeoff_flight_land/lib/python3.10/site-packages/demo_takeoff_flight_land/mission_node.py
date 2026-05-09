import math
from copy import deepcopy

import rclpy
from geometry_msgs.msg import PoseStamped
from mavros_msgs.msg import State
from mavros_msgs.srv import CommandBool, CommandTOL, SetMode
from rclpy.duration import Duration
from rclpy.node import Node
from rclpy.qos import QoSProfile, QoSReliabilityPolicy


class MissionNode(Node):
    def __init__(self) -> None:
        super().__init__("mission_node")

        self.takeoff_alt = 3.0
        self.forward_dist = 3.0
        self.position_tolerance = 0.3

        self.current_state: State | None = None
        self.current_pose: PoseStamped | None = None
        self.target_pose: PoseStamped | None = None

        self.mode_set = False
        self.takeoff_sent = False
        self.landing_sent = False
        self.mission_stage = "INIT"
        self.takeoff_start_time = None

        self.state_sub = self.create_subscription(
            State, "/mavros/state", self.state_cb, 10
        )
        pose_qos = QoSProfile(depth=10)
        pose_qos.reliability = QoSReliabilityPolicy.BEST_EFFORT
        self.pose_sub = self.create_subscription(
            PoseStamped, "/mavros/local_position/pose", self.pose_cb, pose_qos
        )
        self.setpoint_pub = self.create_publisher(
            PoseStamped, "/mavros/setpoint_position/local", 10
        )

        self.set_mode_cli = self.create_client(SetMode, "/mavros/set_mode")
        self.arming_cli = self.create_client(CommandBool, "/mavros/cmd/arming")
        self.takeoff_cli = self.create_client(CommandTOL, "/mavros/cmd/takeoff")
        self.land_cli = self.create_client(CommandTOL, "/mavros/cmd/land")

        self.setpoint_timer = self.create_timer(0.2, self.publish_setpoint)
        self.mission_timer = self.create_timer(0.5, self.step_mission)

        self.get_logger().info("Mission node started")

    def state_cb(self, msg: State) -> None:
        self.current_state = msg

    def pose_cb(self, msg: PoseStamped) -> None:
        self.current_pose = msg

    def publish_setpoint(self) -> None:
        if self.target_pose is None:
            return
        self.target_pose.header.stamp = self.get_clock().now().to_msg()
        self.target_pose.header.frame_id = "map"
        self.setpoint_pub.publish(self.target_pose)

    def step_mission(self) -> None:
        if self.current_state is None or self.current_pose is None:
            return
        if not self.current_state.connected:
            return

        if self.mission_stage == "INIT":
            self.mission_stage = "READY"

        if self.mission_stage in {"READY", "TAKEOFF", "FLY", "LAND"}:
            if self.current_state.mode != "GUIDED":
                self._set_guided_mode()
                return
            if not self.current_state.armed:
                self._arm_vehicle()
                return

        if self.mission_stage == "READY":
            if self.target_pose is None:
                self.target_pose = deepcopy(self.current_pose)
            if not self._services_ready():
                return
            self.mode_set = True
            if not self.takeoff_sent:
                self._takeoff()
                self.takeoff_sent = True
                self.takeoff_start_time = self.get_clock().now()
                self.mission_stage = "TAKEOFF"
                return

        if self.mission_stage == "TAKEOFF":
            if self.target_pose is not None:
                self.target_pose.pose.position.x = self.current_pose.pose.position.x
                self.target_pose.pose.position.y = self.current_pose.pose.position.y
                self.target_pose.pose.position.z = self.takeoff_alt
            altitude_reached = self.current_pose.pose.position.z >= self.takeoff_alt - 0.3
            time_reached = False
            if self.takeoff_start_time is not None:
                elapsed = self.get_clock().now() - self.takeoff_start_time
                time_reached = elapsed >= Duration(seconds=5.0)
            if altitude_reached or time_reached:
                self.target_pose = deepcopy(self.current_pose)
                self.target_pose.pose.position.x += self.forward_dist
                self.target_pose.pose.position.z = self.takeoff_alt
                self.get_logger().info("Switching to FLY stage")
                self.mission_stage = "FLY"
                return

        if self.mission_stage == "FLY":
            if self._target_reached_xy():
                self.mission_stage = "LAND"
                return

        if self.mission_stage == "LAND":
            if not self.landing_sent:
                self._land()
                self.landing_sent = True
                self.target_pose = None
            if (not self.current_state.armed) or (
                self.current_pose.pose.position.z <= 0.2
            ):
                self.mission_stage = "DONE"


    def _services_ready(self) -> bool:
        return (
            self.set_mode_cli.wait_for_service(timeout_sec=0.1)
            and self.arming_cli.wait_for_service(timeout_sec=0.1)
            and self.takeoff_cli.wait_for_service(timeout_sec=0.1)
            and self.land_cli.wait_for_service(timeout_sec=0.1)
        )

    def _set_guided_mode(self) -> None:
        req = SetMode.Request()
        req.custom_mode = "GUIDED"
        self.set_mode_cli.call_async(req)

    def _arm_vehicle(self) -> None:
        req = CommandBool.Request()
        req.value = True
        self.arming_cli.call_async(req)


    def _takeoff(self) -> None:
        req = CommandTOL.Request()
        req.altitude = float(self.takeoff_alt)
        req.latitude = 0.0
        req.longitude = 0.0
        req.min_pitch = 0.0
        req.yaw = 0.0
        self.takeoff_cli.call_async(req)

    def _land(self) -> None:
        req = CommandTOL.Request()
        req.altitude = 0.0
        req.latitude = 0.0
        req.longitude = 0.0
        req.min_pitch = 0.0
        req.yaw = 0.0
        self.land_cli.call_async(req)

    def _target_reached_xy(self) -> bool:
        if self.target_pose is None or self.current_pose is None:
            return False
        dx = self.target_pose.pose.position.x - self.current_pose.pose.position.x
        dy = self.target_pose.pose.position.y - self.current_pose.pose.position.y
        return math.hypot(dx, dy) <= self.position_tolerance


def main() -> None:
    rclpy.init()
    node = MissionNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
