#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import serial
from std_msgs.msg import String
from std_msgs.msg import Byte
from std_msgs.msg import Int16
class Motor_claw(Node):

    def __init__(self):
        super().__init__("motor_claw")
        self.publisher_ = self.create_publisher(Twist, "/robotix/claw_end", 10)
        #self.subscriber_ = self.create_subscription(Twist, "/robotix/cmd_claw", self.my_callback, 10)
        self.subscriber_ = self.create_subscription(Int16, "/robotix/choice", self.my_callback, 10)
        #self.timer_ = self.create_timer(10, self.my_publish)
        self.ser_ = serial.Serial("/dev/ttyACM0", 9600)
        #self.rentrer = 0
        self.fin_claw = 0
        self.get_logger().info("Hello from motor_claw")

    def my_callback(self, choice:Int16):
        if choice == 3 :
            msg = "Lpsortir*"
            print(msg)
            msg_byte = Byte()
            msg_byte = bytes(msg, 'utf-8')
            print(msg_byte)
            self.ser_.write(msg_byte)
            print("I send the Byte")
            #self.rentrer = 1
            #attend jusqu a message de fin de claw
            while not (self.ser_.read(self.nb_bytes).decode('utf-8') == "fin") :
                self.fin_claw = 0
            
            self.my_publish()

    def my_publish(self):
        self.fin_claw = 1
        self.publisher_.publish(self.fin_claw)


def main(args=None):
    rclpy.init(args=args)
    node = Motor_claw()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
