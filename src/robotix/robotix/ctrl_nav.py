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
        self.publisher = self.create_publisher(Int16, '/robotix/reached_pos', 10)
        self.publisher_cmd_pos = self.create_publisher(String, "/robotix/cmd_pos", 10)
        self.subscriber_choice = self.create_subscription(Int16, "/robotix/choice", self.my_callback_choice, 10)
        self.subscriber_real_pos = self.create_subscription(Twist, "/robotix/real_pos", self.my_callback_real_pos, 10)
        self.subscriber_lidar_ = self.create_subscription(LaserScan, "/scan", self.my_callback_lidar, 10)
        self.get_logger().info("Hello from ctrl_nav")
        self.tab_coord_x = [302, 480, 605]
        self.tab_coord_y = [350, 500, 700]
        self.pos_x = 241
        self.pos_y = 268
        self.angle_abs = 0
        self.cmd_distance = 0
        self.cmd_angle = 0
        self.index = 0
        self.distance_rel = 0
        self.choice = 1
        self.distance_plante_1 = []
        self.distance_plante_2 = []
        self.distance_plante_3 = []
        self.angle_plante_1 = []
        self.angle_plante_2 = []
        self.angle_plante_3 = []
        self.calculer_angle_distance(self.pos_x, self.pos_y, self.angle_abs, self.tab_coord_x[0], self.tab_coord_y[0])
        self.my_publish()



    def my_publish_reached_pos(self):
        reached = Int16()
        reached = 0
        if (self.index == 2):
            reached = 1 #un pour dire qu'on a atteint la position
        self.publisher.publish(reached)

    def my_publish(self):
        msg = String()
        if self.choice == 1 or self.choice == 2:
            if self.cmd_angle >= 0:
                #msg.data = "D{}P{}F".format(int(self.cmd_distance),
                #                           int(self.cmd_angle))
                str_var1 = f"{int(self.cmd_distance):04d}"  # Formatage sur 4 caractères
                str_var2 = f"{int(self.cmd_angle):03d}"  # Formatage sur 3 caractères
                msg.data = f"D{str_var1}P{str_var2}F"
            else:
                #msg.data = "D{}N{}F".format(int(self.cmd_distance),
                 #                          int(self.cmd_angle))
                str_var1 = f"{int(self.cmd_distance):04d}"  # Formatage sur 4 caractères
                str_var2 = f"{int(self.cmd_angle):03d}"  # Formatage sur 3 caractères
                msg.data = f"D{str_var1}N{str_var2}F"
            print(msg.data)
            self.publisher_cmd_pos.publish(msg)
            self.index += 1
            #print(self.positions_tab_)
        elif self.choice == 0:
            msg.date = "D{0000}N{000}F" #msg d'arrêt lidar
    def my_callback_choice(self, choice:Int16):
        self.choice = choice

    def trouver_indice_plus_petite_valeur(tableau):
        indice_plus_petite_valeur = 1  # Supposons que le premier élément a la plus petite valeur

        for i in range(1, len(tableau)):
            if tableau[i] < tableau[indice_plus_petite_valeur]:
                # Met à jour l'indice si la valeur actuelle est plus petite
                indice_plus_petite_valeur = i

        return indice_plus_petite_valeur
    def my_callback_real_pos(self, real_pos: Twist):
        self.my_publish_reached_pos()
        self.determine_real_pos(real_pos)
        if self.choice == 1 :
            #self.calculer_angle_distance(self.tab_coord_x[self.index + 1], self.tab_coord_y[self.index + 1], self.angle_abs,
                                        #self.tab_coord_x[self.index + 2], self.tab_coord_y[self.index + 2])
            self.calculer_angle_distance(self.pos_x, self.pos_y, self.angle_abs,
                                         self.tab_coord_x[self.index], self.tab_coord_y[self.index])
        if self.choice == 2 :
            i = self.trouver_indice_plus_petite_valeur(self.distance_plante_2)
            self.cmd_distance = self.distance_plante_2[i] * 10 - 100
            self.cmd_angle = self.angle_plante_2[i]
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
        self.pos_x = self.pos_x + real_pos.linear.x * math.cos(math.radians(real_pos.angular))
        self.pos_y = self.pos_y + real_pos.linear.x * math.sin(math.radians(real_pos.angular))

        #self.pox_x_abs[self.index + 1] = self.pox_x_abs[self.index] + real_pos.linear.x * math.cos(math.radians(real_pos.angular))
        #self.tab_coord_y[self.index + 1] = self.tab_coord_y[self.index] + real_pos.linear.x * math.sin(math.radians(real_pos.angular))
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

    def my_callback_lidar(self, laser: LaserScan):

        self.extract_consecutive_nonzero_values(laser)
        ranges = laser.ranges
        nombre_de_valeurs = len(ranges)
        # Afficher le résultat
        print("Le nombre de valeurs dans le tableau est :", nombre_de_valeurs, "\n")
        print("Valeurs du tableau ranges :", ranges, "\n")

        print("Valeurs du tableau distance_plante_1 :", self.distance_plante_1, "\n")
        print("Valeurs du tableau distance_plante_2 :", self.distance_plante_2, "\n")
        print("Valeurs du tableau distance_plante_3 :", self.distance_plante_3, "\n")

        print("Valeurs du tableau angle_plante_1 :", self.angle_plante_1, "\n")
        print("Valeurs du tableau angle_plante_2 :", self.angle_plante_2, "\n")
        print("Valeurs du tableau angle_plante_3 :", self.angle_plante_3, "\n")

        print("\n")

        self.distance_plante_1.clear()
        self.distance_plante_2.clear()
        self.distance_plante_3.clear()

        self.angle_plante_1.clear()
        self.angle_plante_2.clear()
        self.angle_plante_3.clear()

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
                if (last_value != 0.0) and (value== 0.0):
                    number_sequence += 1
                if value != 0 :
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


            #if(len(self.angle_plante_1) <= 3 or len(self.angle_plante_2) <= 3 or len(self.angle_plante_3) <= 3):
            #    self.my_callback_lidar(laser)

            number_samples = len(ranges)
            angle_increment = 100/(number_samples-1)
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
