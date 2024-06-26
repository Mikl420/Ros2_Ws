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
        #self.subscriber_emergency = self.create_subscription(String, "/robotix/stop", self.my_callback_stop, 10)
        #self.timer_ = self.create_timer(5.0, self.my_publish)
        self.ser_ = serial.Serial("/dev/ttyACM0", 115200)
        self.get_logger().info("Hello from motor")

    def my_callback(self, pos: String):
        print("I'm in callback motor")
        msg = String
        msg = pos.data
        #print(msg)
        msg_byte = Byte()
        msg_byte = bytes(msg, 'utf-8')
        #print(msg_byte)
        if self.ser_.write(msg_byte):
            print("I sended the Byte ", msg_byte, "\n")
        else : 
            print("Failed to send")
    def my_callback_stop(self, pos: String):
        msg = String
        msg = pos.data
        msg_byte = Byte()
        msg_byte = bytes(msg, 'utf-8')
        if self.ser_.write(msg_byte):
            print("I sended the Byte ", msg_byte, "\n")
    def my_publish(self):
        pass

def main(args=None):
    rclpy.init(args=args)
    node = Motor()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
