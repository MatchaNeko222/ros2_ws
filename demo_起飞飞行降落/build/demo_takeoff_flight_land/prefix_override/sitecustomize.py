import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/luckiop/IDEA_learn_ws/ros2_ws/demo_起飞飞行降落/install/demo_takeoff_flight_land'
