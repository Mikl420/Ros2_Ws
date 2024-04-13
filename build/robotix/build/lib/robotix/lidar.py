#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Int16

class Lidar(Node):

    def __init__(self):
        super().__init__("lidar")
        self.publisher_ = self.create_publisher(Twist, "/robotix/lidar", 10)
        self.subscriber_ = self.create_subscription(Twist, "/robotix/topic", self.my_callback, 10)
        self.timer_ = self.create_timer(0.5, self.my_publish)
        self.get_logger().info("Hello from lidar")

    def my_callback(self):
        pass

    def my_publish(self):
        pass

def main(args=None):
    rclpy.init(args=args)
    node = Lidar()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
