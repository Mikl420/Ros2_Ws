
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
from rclpy.executors import ExternalShutdownException
import subprocess
import math
import time

class Ctrl_nav(Node):

    def __init__(self):
        super().__init__("ctrl_nav")
        self.publisher_cmd_pos = self.create_publisher(String, "/robotix/cmd_pos", 10)
        self.publisher_claw = self.create_publisher(String, "/robotix/ctrl_claw", 10)
        #self.timer_ = self.create_timer(3.0, self.my_publish)
        self.subscriber_choice = self.create_subscription(Int16, "/robotix/choice", self.my_callback_choice, 10)
        self.subscriber_real_pos = self.create_subscription(Int16, "/robotix/real_pos", self.my_callback_real_pos, 10)
        self.subscriber_lidar_ = self.create_subscription(LaserScan, "/scan", self.my_callback_lidar, 10)
        self.subscriber_claw = self.create_subscription(Int16, "/robotix/serial_pince", self.my_callback_real_pos, 10)
        #self.timer = self.create_timer(5.0, self.check_message_received)
        self.get_logger().info("Hello from ctrl_nav")
        self.angle_abs = 0
        self.cmd_distance = 0
        self.cmd_angle = 0
        self.index = 0
        self.distance_rel = 1
        self.tab_cmd = ["D0380P090", "D0320N090"]
        self.choice = 1
        self.msg = String()
        self.extracted_angle = "P000"
        self.msg.data = "D0001P000"
        self.msg_claw = String()
        self.last_msg = String()
        #self.msg.data = self.tab_cmd[self.index]
        self.my_publish()
        self.distance_plante = []
        self.angle_plante = []
        self.distance_plante_1 = [50]         
        self.distance_plante_2 = [50]
        self.distance_plante_3 = [50]
        self.angle_plante_1 = [50]         
        self.angle_plante_2 = [50]
        self.angle_plante_3 = [50]
        self.distance_plantes = []
        self.angle_plantes = []
        self.determination = 0
        self.flag_lidar = True
        self.received_message = False
        self.plante1 = False
        self.plante2 = False
        self.plante3 = False
        self.min_plante1 = 0
        self.min_plante2 = 0
        self.min_plante3 = 0
        self.startTime= 0

    def my_publish(self):
        print(self.msg.data)
        self.publisher_cmd_pos.publish(self.msg)
        print("publish done")

    def my_publish_claw(self):
        print(self.msg_claw.data)
        self.publisher_claw.publish(self.msg_claw)

    def my_callback_choice(self, choice:Int16):
        self.choice = choice

    def my_callback_real_pos(self, arrived:Int16):
        if self.startTime>time.time():
            raise RuntimeError
        print("TIME ====" + str(time.time()))
        if self.received_message == False:
            print('Message RECEIVED')
            self.received_message = True
        self.index += 1
        print("INDEX", self.index)
        if self.index == 1 :
            self.msg.data = self.tab_cmd[self.index-1]
            self.my_publish()

        if self.index == 2:
            self.msg.data = self.tab_cmd[self.index-1]
            self.my_publish()

        if self.index == 4:
            self.flag_lidar == True
            self.msg_claw.data = 'PF1'
            self.my_publish_claw()

        if self.index == 5:
            self.last_msg.data = self.msg.data
            self.msg.data = "D0120P000"
            self.my_publish()
        
        if self.index == 6:
            self.msg_claw.data = 'PF2'
            self.my_publish_claw()
        
        if self.index == 7 :
            self.msg_claw.data = 'DP'
            self.my_publish_claw()
        
        #if self.index == 7:
            self.msg.data = "R0120N000"
            self.my_publish()

        #if self.index == 8:
            self.distance_plante_1 = [50]         
            self.distance_plante_2 = [50]
            self.distance_plante_3 = [50]
            self.angle_plante_1 = [50]         
            self.angle_plante_2 = [50]
            self.angle_plante_3 = [50]
            self.flag_lidar = True
            self.msg.data = self.last_msg.data
            self.rewind_after_lidar()
            self.my_publish()
            self.msg.data = "D0000" + str(self.extracted_angle)
            self.my_publish()
        """"
        if self.index == 10:
            if self.plante1:
                if self.min_plante2 < self.min_plante3:
                    self.distance_plante = self.distance_plante_2
                    self.angle_plante = self.angle_plante_2
                else:
                    self.distance_plante = self.distance_plante_3
                    self.angle_plante = self.angle_plante_3
            
            if self.plante2:
                if self.min_plante1 < self.min_plante2:
                    self.distance_plante = self.distance_plante_1
                    self.angle_plante = self.angle_plante_1
                else:
                    self.distance_plante = self.distance_plante_3
                    self.angle_plante = self.angle_plante_3
            
            if self.plante3:
                if self.min_plante1 < self.min_plante2:
                    self.distance_plante = self.distance_plante_1
                    self.angle_plante = self.angle_plante_1
                else:
                    self.distance_plante = self.distance_plante_2
                    self.angle_plante = self.angle_plante_2
            i1 = self.trouver_indice_plus_petite_valeur(self.distance_plante)
            self.plante_format((self.distance_plante[i1]) * 1000, self.angle_plante[i1])
            self.my_publish()
        """
        if self.index == 12 :
            self.msg_claw.data = 'PF1'
            self.my_publish_claw()
        
        if self.index == 13:
            self.last_msg.data = self.msg.data
            self.msg.data = "D0120P000"
            self.my_publish()
                
        if self.index == 14:
            self.msg_claw.data = 'PF2'
            self.my_publish_claw()
        
        if self.index == 15:
            self.msg.data = "R0120P000"
            self.my_publish()
            self.msg_claw.data = 'DP'
            self.my_publish_claw()
        
        #if self.index == 15:
            #self.msg.data = "R0120P000"
            #self.my_publish()

        #if self.index == 15:
            self.distance_plante_1 = [50]         
            self.distance_plante_2 = [50]
            self.distance_plante_3 = [50]
            self.angle_plante_1 = [50]         
            self.angle_plante_2 = [50]
            self.angle_plante_3 = [50]
            self.flag_lidar = True
            self.msg.data = self.last_msg.data
            self.rewind_after_lidar()
            self.my_publish()
            self.msg.data = "D0000" + str(self.extracted_angle)
            self.my_publish()

        if self.index == 20:
            self.msg_claw.data = 'PF1'
            self.my_publish_claw()

        if self.index == 21:
            self.last_msg.data = self.msg.data
            self.msg.data = "D0120P000"
            self.my_publish()
                
        if self.index == 22 :
            self.msg_claw.data = 'PF2'
            self.my_publish_claw()
        
        if self.index == 23:
            self.msg_claw.data = 'DP'
            self.my_publish_claw()
            self.msg.data = "R0120P000"
            self.my_publish()
            self.msg.data = self.last_msg.data
            self.distance_plante_1 = [50]         
            self.distance_plante_2 = [50]
            self.distance_plante_3 = [50]
            self.angle_plante_1 = [50]         
            self.angle_plante_2 = [50]
            self.angle_plante_3 = [50]
            self.rewind_after_lidar()
            self.my_publish()
            self.msg.data = "D0000" + self.extracted_angle
            self.my_publish()
        
        #if self.index == 20:
        #    self.msg.data = "R0120P000"
        #    self.my_publish()

        #if self.index == 22:
        #    self.msg.data = self.last_msg.data
        #    self.distance_plante_1 = [50]         
        #    self.distance_plante_2 = [50]
        #    self.distance_plante_3 = [50]
        #    self.angle_plante_1 = [50]         
        #    self.angle_plante_2 = [50]
        #    self.angle_plante_3 = [50]
        #    self.rewind_after_lidar()
        #    self.my_publish()

        if self.index == 27:
            self.msg.data = "R0320P000"
            self.my_publish()
        
        if self.index == 28:
            self.msg.data = "D0380N090"
            self.my_publish()
        
        #if self.index == 24:
            self.msg_claw.data = "RP"
            self.my_publish_claw()
        
        if self.index == 29:
            self.msg.data = "R0100P000"
            self.my_publish()

        if self.index == 30:
            self.msg_claw.data = "DF2"
            self.my_publish_claw()

        if self.index == 31:
            self.msg_claw.data = "RP"
            self.my_publish_claw()

        if self.index == 32:
            self.msg.data = "R0100P000"
            self.my_publish()

        if self.index == 33:
            self.msg_claw.data = "DF2"
            self.my_publish_claw()
        
        if self.index == 34:
            self.msg_claw.data = "RP"
            self.my_publish_claw()

        if self.index == 35:
            self.msg.data = "R0100P000"
            self.my_publish()

        #if self.index == 33:
            self.msg_claw.data = "DF2"
            self.my_publish_claw()

        #if self.index == 34:
            self.msg.data = "R1040P000"
            self.my_publish()  

    def rewind_after_lidar(self):
        if self.msg.data[5] == "N":
            modified_data = self.msg.data.replace("D", "R")
            modified_data2 = modified_data.replace("N", "P")
            self.msg.data = modified_data2
            self.extracted_angle = String(self.msg.data[5:8])
            self.msg.data = self.msg.data[:5] + "P000"
            print("Modified data", modified_data2)
            #self.msg.data.replace("D", "R")
            #self.msg.data.replace("N", "P")
        else:
            modified_data = self.msg.data.replace("D", "R")
            modified_data2 = modified_data.replace("P", "N")
            self.msg.data = modified_data2
            print("Modified data", modified_data2)
            #self.msg.data.replace("D", "R")
            #self.msg.data.replace("P", "N")
        print("REWIND",self.msg.data)
    def trouver_indice_plus_petite_valeur(self,tableau):
        indice_plus_petite_valeur = 1  # Supposons que le premier élément a la plus petite valeur
        for i in range(1, len(tableau)):
            if tableau[i] < tableau[indice_plus_petite_valeur]:
                # Met à jour l'indice si la valeur actuelle est plus petite
                indice_plus_petite_valeur = i

        return indice_plus_petite_valeur

    def plante_format(self, distance, angle):
        #msg = String()
        if angle >= 10 :
            str_var1 = f"{round(distance-195):04d}"  # Formatage sur 4 caractères
            str_var2 = f"{round(angle*0.8):03d}"  # Formatage sur 3 caractères
            self.msg.data = f"D{str_var1}N{str_var2}"
            print("negatif")
        if angle < 10 and  angle > 0:
            angle = angle - 2
            str_var1 = f"{round(distance-195):04d}"  # Formatage sur 4 caractères
            str_var2 = f"{round(angle):03d}"  # Formatage sur 3 caractères
            self.msg.data = f"D{str_var1}N{str_var2}"
            print("petit negatif")

        if angle <= -10:
            str_var1 = f"{round(distance-195):04d}"  # Formatage sur 4 caractères
            str_var2 = f"{round(abs(angle*0.7)):03d}"  # Formatage sur 3 caractères
            self.msg.data = f"D{str_var1}P{str_var2}"
            print("positif")

        if angle > -10 and angle < 0:
            angle = angle + 2
            str_var1 = f"{round(distance-195):04d}"  # Formatage sur 4 caractères
            str_var2 = f"{round(abs(angle)):03d}"  # Formatage sur 3 caractères
            self.msg.data = f"D{str_var1}P{str_var2}"
            print("petit positif")
        print("PLANTE FORMAT",self.msg.data)


    def my_callback_lidar(self, laser: LaserScan):
        if (self.index == 3 or self.index == 10 or self.index == 18) and self.flag_lidar:
            self.flag_lidar = False
            print("CallbackLIDAR")
            delay =0
            while(delay<900000):
                delay+=1
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
### new code
            # Calcul des minimums
            self.min_plante1 = min(self.distance_plante_1)
            self.min_plante2 = min(self.distance_plante_2)
            self.min_plante3 = min(self.distance_plante_3)
            # Détermination du tableau avec la valeur la plus petite
            if self.min_plante1 < self.min_plante2 and self.min_plante1 < self.min_plante3:
                self.distance_plante = self.distance_plante_1
                self.angle_plante = self.angle_plante_1 
                self.plante1 = True
            elif self.min_plante2 < self.min_plante3:
                self.distance_plante = self.distance_plante_2
                self.angle_plante = self.angle_plante_2
                self.plante2 = True
            else:
                self.distance_plante = self.distance_plante_3
                self.angle_plante = self.angle_plante_3
                self.plante3 = True 
### end user code
            i1=self.trouver_indice_plus_petite_valeur(self.distance_plante)
            print("Indice tableau",i1)
            self.plante_format((self.distance_plante[i1])*1000, self.angle_plante[i1])
            print(self.angle_plante[i1])
            self.my_publish()

    def extract_consecutive_nonzero_values(self, laser: LaserScan):
        ranges = laser.ranges
        print(ranges)
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
            if value != 0 and last_value !=0:
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
            self.angle_plante_1[i] = self.angle_plante_1[i] * angle_increment -63

        for i in range(len(self.angle_plante_2)):
            self.angle_plante_2[i] = self.angle_plante_2[i] * angle_increment -63

        for i in range(len(self.angle_plante_3)):
            self.angle_plante_3[i] = self.angle_plante_3[i] * angle_increment -63


    def check_message_received(self):
        if not self.received_message:
            self.get_logger().info('ExternalShutdownException')
            raise ExternalShutdownException('ExternalShutdownException')  # Ceci va arrêter le nœud
        else:
            self.get_logger().info('Message reçu, exécution normale.')
    
    def setEndTime(self, time):
        self.startTime = time + 95 

def main(args=None):
    rclpy.init(args=args)
    node = Ctrl_nav()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()

