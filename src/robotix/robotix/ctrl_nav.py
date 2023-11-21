#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Int16
import sensor_msgs
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String
from std_msgs.msg import Int32MultiArray
import math

class Ctrl_nav(Node):

    def __init__(self):
        super().__init__("ctrl_nav")
        self.publisher_cmd_pos = self.create_publisher(String, "/robotix/cmd_pos", 10)
        self.subscriber_choice = self.create_subscription(Int16, "/robotix/choice", self.my_callback_choice, 10)
        self.subscriber_real_pos = self.create_subscription(Twist, "/robotix/real_pos", self.my_callback_real_pos, 10)
        self.subscriber_lidar_ = self.create_subscription(LaserScan, "/scan", self.my_callback_cmd_pos, 10)
        self.get_logger().info("Hello from ctrl_nav")
        self.pos_x_abs = [0, 100, 200]
        self.pos_y_abs = [0, 100, 200]
        self.angle_abs = 0
        self.cmd_distance = 0
        self.cmd_angle = 0
        self.index = 0
        self.distance_rel = 0
        self.choice = 1

    def my_publish(self):
        msg = String()
        if self.choice == 1:
            if self.cmd_angle >= 0:
                msg.data = "D{}P{}F".format(int(self.cmd_distance),
                                           int(self.cmd_angle))
            else:
                msg.data = "D{}N{}F".format(int(self.cmd_distance),
                                           int(self.cmd_angle))
            print(msg.data)
            self.publisher_cmd_pos.publish(msg)
            self.index += 1
            print(self.positions_tab_)
        elif self.choice == 0:
            msg.date = "D{0000}N{000}F" #msg d'arrêt lidar
    def my_callback_choice(self, choice:Int16):
        self.choice = choice
    def my_callback_real_pos(self, real_pos: Twist):
        self.determine_real_pos(real_pos)
        self.calculer_angle_distance(self.pos_x_abs[self.index + 1], self.pos_y_abs[self.index + 1], self.angle_abs,
                                     self.pos_x_abs[self.index + 2], self.pos_y_abs[self.index + 2])
        self.my_publish()
#    def my_callback_cmd_pos(self, scan:LaserScan):
#        print("The Array of ranges is: ", scan.ranges)
#        print("The first value is : ", scan.ranges[1])
#        alerte_collision = False
#        for x in scan.ranges:
#            if scan.ranges != 0.0 and alerte_collision == False:
#                alerte_collision = True
#
#        if alerte_collision:
#            print("Robot must be stopped ")
#           self.my_publish()
#        else :
#            self.my_publish()
#        pass

    def determine_real_pos(self, real_pos: Twist):
        self.angle_abs += real_pos.angular
        self.pox_x_abs[self.index + 1] = self.pox_x_abs[self.index] + real_pos.linear.x * math.cos(math.radians(real_pos.angular))
        self.pos_y_abs[self.index + 1] = self.pos_y_abs[self.index] + real_pos.linear.x * math.sin(math.radians(real_pos.angular))
        #real_pos.linear.x c'est la distance reçue des codeuses.

    def calculer_angle_distance(self, x_depart, y_depart, orientation_depart, x_destination, y_destination):
        # Calculer la différence en x et en y entre les points de départ et d'arrivée
        delta_x = x_destination - x_depart
        delta_y = y_destination - y_depart

        # Calculer la distance entre les points de départ et d'arrivée
        self.cmd_distance = math.sqrt(delta_x ** 2 + delta_y ** 2)

        # Calculer l'angle entre les deux points en radians
        angle_radians = math.atan2(delta_y, delta_x)

        # Convertir l'angle en degrés
        angle_degrees = math.degrees(angle_radians)

        # Calculer l'angle de rotation nécessaire pour atteindre la nouvelle orientation
        self.cmd_angle = angle_degrees - orientation_depart



def main(args=None):
    rclpy.init(args=args)
    node = Ctrl_nav()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
