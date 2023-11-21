from setuptools import find_packages, setup

package_name = 'robotix'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='robotix',
    maintainer_email='robotix@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "controller= robotix.controller:main",
            "lidar= robotix.lidar:main",
            "ctrl_nav= robotix.ctrl_nav:main",
            "jetson= robotix.jetson:main",
            "ctrl_claw= robotix.ctrl_claw:main",
            "laser= robotix.laser:main",
            "motor_claw= robotix.motor_claw:main",
            "motor= robotix.motor:main",
            "codeuse= robotix.codeuse:main",
            "motor_plateau= robotix.motor_plateau:main"
        ],
    },
)
