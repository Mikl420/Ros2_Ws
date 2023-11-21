#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Int16
class Motor_claw(Node):

    def __init__(self):
        super().__init__("motor_claw")
        self.publisher_ = self.create_publisher(Twist, "/robotix/claw_end", 10)
        self.subscriber_ = self.create_subscription(Twist, "/robotix/cmd_claw", self.my_callback, 10)
        self.timer_ = self.create_timer(0.5, self.my_publish)
        self.get_logger().info("Hello from motor_claw")

    def my_callback(self):
        pass

    def my_publish(self):
        pass

def main(args=None):
    rclpy.init(args=args)
    node = Motor_claw()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
