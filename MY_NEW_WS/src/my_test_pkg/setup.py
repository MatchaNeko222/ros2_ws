import os
from glob import glob

from setuptools import find_packages, setup

package_name = 'my_test_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='haruka',
    maintainer_email='haruka@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            "publisher = my_test_pkg.publisher:main",
            "subscriber = my_test_pkg.subscriber:main",
            "simple_service = my_test_pkg.simple_service:main",
            "simple_client = my_test_pkg.simple_client:main",
            "person_info_publisher = my_test_pkg.person_info_publisher:main",
            "person_info_subscriber = my_test_pkg.person_info_subscriber:main",
            "person_info_param_publisher = my_test_pkg.person_info_param_publisher:main",
        ],
    },
)
