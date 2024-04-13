#!/usr/bin/env python3
import rclpy
#import rospy
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
        #self.timer_ = self.create_timer(3.0, self.my_publish)
        self.subscriber_choice = self.create_subscription(Int16, "/robotix/choice", self.my_callback_choice, 10)
        self.subscriber_real_pos = self.create_subscription(Int16, "/robotix/real_pos", self.my_callback_real_pos, 10)
        self.subscriber_lidar_ = self.create_subscription(LaserScan, "/scan", self.my_callback_lidar, 10)
        self.get_logger().info("Hello from ctrl_nav")
        self.angle_abs = 0
        self.cmd_distance = 0
        self.cmd_angle = 0
        self.index = 0
        self.distance_rel = 1
        self.tab_cmd = ["D0380P090", "D0320N090"]#, "D0000P000"
        self.choice = 1
        self.my_publish()
        self.distance_plante_1 = []
        self.distance_plante_2 = []
        self.distance_plante_3 = []
        self.angle_plante_1 = []
        self.angle_plante_2 = []
        self.angle_plante_3 = []
        self.distance_plantes = []
        self.angle_plantes = []
        self.determination = 0
        self.msg=String()

    def my_publish(self):
        msg = String()
        if self.choice == 1 :
            msg.data = self.tab_cmd[self.index]
            print(msg.data)
            self.publisher_cmd_pos.publish(msg)
            self.index += 1

    def my_callback_choice(self, choice:Int16):
        self.choice = choice

    def my_callback_real_pos(self, arrived:Int16):
        if self.index == 2:
            i1=self.trouver_indice_plus_petite_valeur(self.distance_plante_1)
            self.plante_format((self.distance_plante_1[i1])*10+90, self.angle_plante_1[i1])
            self.index +=1
           # rclpy.sleep(5)
        elif self.index == 3:
            if self.msg.data[6]=="N":
                self.msg.data.replace("D","R")
                self.msg.data.replace("N","P")
            else:
                self.msg.data.replace("D","R")
                self.msg.data.replace("P","N")
            print(self.msg.data)
            self.publisher_cmd_pos.publish(self.msg)
            self.index += 1
        else :
            self.my_publish()


    def trouver_indice_plus_petite_valeur(self,tableau):
        indice_plus_petite_valeur = 1  # Supposons que le premier élément a la plus petite valeur

        for i in range(1, len(tableau)):
            if tableau[i] < tableau[indice_plus_petite_valeur]:
                # Met à jour l'indice si la valeur actuelle est plus petite
                indice_plus_petite_valeur = i

        return indice_plus_petite_valeur

    def plante_format(self, distance, angle):
        #msg = String()
        if angle >= 0:
            str_var1 = f"{int(distance):04d}"  # Formatage sur 4 caractères
            str_var2 = f"{int(angle-5):03d}"  # Formatage sur 3 caractères
            self.msg.data = f"D{str_var1}N{str_var2}"

        else:
            str_var1 = f"{int(distance):04d}"  # Formatage sur 4 caractères
            str_var2 = f"{int(abs(angle+3)):03d}"  # Formatage sur 3 caractères
            self.msg.data = f"D{str_var1}P{str_var2}"
        print(self.msg.data)
        self.publisher_cmd_pos.publish(self.msg)

    def my_callback_lidar(self, laser: LaserScan):
        if self.index ==2:
            self.extract_consecutive_nonzero_values(laser)
            #ranges = laser.ranges
            #nombre_de_valeurs = len(ranges)
            # Afficher le résultat
            #print("Le nombre de valeurs dans le tableau est :", nombre_de_valeurs, "\n")
            #print("Valeurs du tableau ranges :", ranges, "\n")

            print("Valeurs du tableau distance_plante_1 :", self.distance_plante_1, "\n")
            print("Valeurs du tableau distance_plante_2 :", self.distance_plante_2, "\n")
            print("Valeurs du tableau distance_plante_3 :", self.distance_plante_3, "\n")

            print("Valeurs du tableau angle_plante_1 :", self.angle_plante_1, "\n")
            print("Valeurs du tableau angle_plante_2 :", self.angle_plante_2, "\n")
            print("Valeurs du tableau angle_plante_3 :", self.angle_plante_3, "\n")

            print("\n")

            #self.distance_plante_1.clear()
            #self.distance_plante_2.clear()
            #self.distance_plante_3.clear()

            #self.angle_plante_1.clear()
            #self.angle_plante_2.clear()
            #self.angle_plante_3.clear()

    def extract_consecutive_nonzero_values(self, laser: LaserScan):
        ranges = laser.ranges

        for i in range(1, len(ranges) - 1):
            if ranges[i] == 0 and ranges[i - 1] != 0 and ranges[i + 1] != 0:
                moyenne = (ranges[i - 1] + ranges[i + 1]) / 2.0
                ranges[i] = moyenne

        number_sequence = 0
        last_value = 0.0
        last_last_value = 0.0
        for index, value in enumerate(ranges):
            if (last_value != 0.0) and (value == 0.0):
                number_sequence += 1
            if value != 0:
                match number_sequence:
                    case 0:
                        self.distance_plante_1.append(value)
                        self.angle_plante_1.append(index)
                    case 1:
                        self.distance_plante_2.append(value)
                        self.angle_plante_2.append(index)
                    case 2:
                        self.distance_plante_3.append(value)
                        self.angle_plante_3.append(index)
            last_last_value = last_value
            last_value = value

        # if(len(self.angle_plante_1) <= 3 or len(self.angle_plante_2) <= 3 or len(self.angle_plante_3) <= 3):
        #    self.my_callback_lidar(laser)

        number_samples = len(ranges)
        angle_increment = 100 / (number_samples - 1)
        for i in range(len(self.angle_plante_1)):
            self.angle_plante_1[i] = self.angle_plante_1[i] * angle_increment - 50

        for i in range(len(self.angle_plante_2)):
            self.angle_plante_2[i] = self.angle_plante_2[i] * angle_increment - 50

        for i in range(len(self.angle_plante_3)):
            self.angle_plante_3[i] = self.angle_plante_3[i] * angle_increment - 50

def main(args=None):
    rclpy.init(args=args)
    node = Ctrl_nav()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
