#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Int16
class Serial_pince(Node):

    def __init__(self):
        super().__init__("serial_pince")
        self.publisher = self.create_publisher(String, "/robotix/serial_pince", 10)
        self.timer_ = self.create_timer(0.2, self.my_publish)
        self.ser_ = serial.Serial("/dev/ttyACM1", 9600)
        self.get_logger().info("Hello from serial_pince")
	

    def my_callback(self):
        pass

    def my_publish(self):
        if (self.data_str[0] == 'M'):
            msg = String()
            self.data_str = self.ser_.read(self.nb_bytes).decode('utf-8')
            self.publisher.publish(self.msg)

def main(args=None):
    rclpy.init(args=args)
    node = Serial_pince()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
