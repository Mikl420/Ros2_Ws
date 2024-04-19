#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Int16
import serial
from std_msgs.msg import String
from std_msgs.msg import Byte
from time import sleep

class Motor(Node):

    def __init__(self):
        super().__init__("motor")
        #self.publisher_ = self.create_publisher(Twist, "/robotix/topic", 10)
        self.subscriber_ = self.create_subscription(String, "/robotix/cmd_pos", self.my_callback, 10)
        #self.timer_ = self.create_timer(5.0, self.my_publish)
        self.ser_ = serial.Serial("/dev/ttyACM1", 9600)
        self.get_logger().info("Hello from motor")

    def my_callback(self, pos: String):
        #print(pos.data)
        msg = String
        msg = pos.data
        #print(msg)
        msg_byte = Byte()
        msg_byte = bytes(msg, 'utf-8')
        #print(msg_byte)
        if self.ser_.write(msg_byte):
            print("I sended the Byte ", msg_byte, "\n")


        #strings = ["D1096N045", "D0696N45", "D0000P178"]
        #byte_array = [s.encode('utf-8') for s in strings]
        #for i in range(len(strings)):
            #self.ser_.write(byte_array[i])
            # Affichez le tableau de bytes
            #print(byte_array)

        #self.get_logger().info("I send A")

    def my_publish(self):
        pass

def main(args=None):
    rclpy.init(args=args)
    node = Motor()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
