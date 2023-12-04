#!/usr/bin/env python3
import rclpy
import std_msgs
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Int16
from std_msgs.msg import String
from std_msgs.msg import Int32MultiArray

class Controller(Node):



    def __init__(self):
        super().__init__("controller")
        self.publisher = self.create_publisher(Int32MultiArray,'/robotix/pos',10)
        self.publisher_ = self.create_publisher(Int16, "/robotix/choice", 10)
        self.subscriber_ = self.create_subscription(Int16, "/robotix/claw_end", self.my_callback_claw, 10)
        self.subscriber_ = self.create_subscription(Twist, "/robotix/real_pos", self.my_callback_pos, 10)
        #self.timer_ = self.create_timer(10.0, self.my_publish)
        self.get_logger().info("Hello from controller")
        self.msg = Int16()
        self.msg.data = 1
        self.publisher_.publish(self.msg)
        self.get_logger().info(self.msg.data)
    def my_publish(self):
        self.publisher_.publish(self.msg)


    def my_callback_claw(self):
        pass

    def my_callback_pos(self, pos: Twist):
        if(pos.linear.)

def main(args=None):
    rclpy.init(args=args)
    node = Controller()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
