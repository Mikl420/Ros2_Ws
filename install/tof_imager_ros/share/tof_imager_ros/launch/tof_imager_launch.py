from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='tof_imager_ros',  # Make sure to replace with your actual package name
            executable='tof_imager_publisher',
            name='tof_imager_publisher'
        )
    ])

