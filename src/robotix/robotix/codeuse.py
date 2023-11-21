#!/usr/bin/env python3
import rclpy
import serial
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Int16
import struct
class Codeuse(Node):

    def __init__(self):
        super().__init__("codeuse")
        self.publisher_ = self.create_publisher(Twist, "/robotix/real_pos", 10)
        self.subscriber_ = self.create_subscription(Twist, "/robotix/real_pos", self.my_callback, 10)
        self.timer_ = self.create_timer(0.5, self.my_publish)
        self.ser_ = serial.Serial("/dev/ttyACM0", 9600)
        self.get_logger().info("Hello from codeuse")
        self.nb_bytes = 9
        self.data_str = bytearray([])

    def my_callback(self):
        self.data_str = self.ser_.read(self.nb_bytes).decode('utf-8')
        if(self.data_str[0] == 'C'):
            self.my_publish()

    def my_publish(self):
        twist = Twist
        twist.linear.x = self.data_str[1:4]
        twist.angular = self.data_str[6:8]
        print("i publish")
        self.publisher_.publish(twist)
def main(args=None):
    rclpy.init(args=args)
    node = Codeuse()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
