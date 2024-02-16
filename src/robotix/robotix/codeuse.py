#!/usr/bin/env python3
import rclpy
import serial
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Int16
import struct
import re
class Codeuse(Node):

    def __init__(self):
        super().__init__("codeuse")
        self.publisher_ = self.create_publisher(Twist, "/robotix/real_pos", 10)
        #self.subscriber_ = self.create_subscription(Twist, "/robotix/real_pos", self.my_callback, 10)
        self.timer_ = self.create_timer(0.2, self.my_publish)
        self.ser_ = serial.Serial("/dev/ttyUSB0", 9600)
        self.get_logger().info("Hello from codeuse")
        self.nb_bytes = 9
        self.data_str = bytearray([])

    def my_callback(self):
        pass

    def my_publish(self):
        self.data_str = self.ser_.read(self.nb_bytes).decode('utf-8')
        print(self.data_str)
        if (self.data_str[0] == 'D'):
            twist = Twist()
            # Utiliser une expression régulière pour extraire les valeurs
            #match = re.match(r'C(\d+)P(\d+)F|C(\d+)N(\d+)F', self.data_str)

            #if match:
                # Utiliser les groupes de correspondance pour extraire les valeurs
            #    twist.linear.x = float(match.group(1) or match.group(3))
            #    twist.angular = float(match.group(2) or match.group(4))
            twist.linear.x =float(self.data_str[1:5])
            twist.linear.y = float(self.data_str[6:9]) #prob conversion string to float
            print(twist.linear.x)
            print(twist.linear.y)
            self.publisher_.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    node = Codeuse()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
