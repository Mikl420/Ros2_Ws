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
        self.publisher_ = self.create_publisher(Int16, "/robotix/choice", 10)
        self.subscriber_ = self.create_subscription(Int16, "/robotix/reached_pos", self.my_callback_reached_pos, 10)
        self.subscriber_ = self.create_subscription(Int16, "/robotix/claw_end", self.my_callback_claw, 10)
        self.subscriber_ = self.create_subscription(Twist, "/robotix/real_pos", self.my_callback_pos, 10)
        #self.timer_ = self.create_timer(10.0, self.my_publish)
        self.get_logger().info("Hello from controller")
        self.msg = Int16()
        self.msg.data = 1
        self.publisher_.publish(self.msg)
    def my_publish(self):
        self.publisher_.publish(self.msg)


    def my_callback_claw(self):
        pass

    def my_callback_pos(self):
        pass

    def my_callback_reached_pos(self, reached: Int16):
        if (reached == 1) :
            self.msg = 2
        self.my_publish()

def main(args=None):
    rclpy.init(args=args)
    node = Controller()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
