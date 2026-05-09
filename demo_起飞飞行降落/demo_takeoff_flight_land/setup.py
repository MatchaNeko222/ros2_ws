from setuptools import setup

package_name = "demo_takeoff_flight_land"

setup(
    name=package_name,
    version="0.0.1",
    packages=[package_name],
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        ("share/" + package_name + "/launch", ["launch/mission.launch.py"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="user",
    maintainer_email="user@example.com",
    description="Takeoff, fly forward 3m, and land using MAVROS in Gazebo.",
    license="Apache-2.0",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "mission_node = demo_takeoff_flight_land.mission_node:main",
        ],
    },
)
