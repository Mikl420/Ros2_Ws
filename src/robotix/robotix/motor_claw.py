#!/usr/bin/env python3
import rclpy
import serial
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Int16
import struct
import re
class Motor_claw(Node):

    def __init__(self):
        super().__init__("codeuse")
        self.publisher_ = self.create_publisher(Int16, "/robotix/serial_pince", 10)
        #self.subscriber_ = self.create_subscription(Twist, "/robotix/real_pos", self.my_callback, 10)
        self.timer_ = self.create_timer(0.2, self.my_publish)
        self.ser_ = serial.Serial("/dev/ttyUSB1", 115200)
        #self.ser_esp = serial.Serial("/dev/ttyUSB0", 9600)
        self.get_logger().info("Hello from serial pince")
        self.nb_bytes = 1
        self.nb_bytes_esp = 9
        self.data_str = bytearray([])
        self.data_str_esp = bytearray([])

    def my_callback(self):
        pass

    def my_publish(self):
        self.data_str = self.ser_.read(self.nb_bytes).decode('utf-8')
        #self.data_str_esp = self.ser_esp.read(self.nb_bytes_esp).decode('utf-8')
        #print(self.data_str)
        #print(self.data_str_esp)
        if (self.data_str[0] == 'M'):
            arrived = Int16()
            self.publisher_.publish(arrived)
            self.get_logger().info("I got the byte")
        #if (self.data_str_esp[0] == 'D'):

def main(args=None):
    rclpy.init(args=args)
    node = Motor_claw()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
