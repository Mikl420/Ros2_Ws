# Notes : Connecter le capteur de démarrage à la broche 18 du Raspberry Pi, brancher l'autre côté à la masse.
import RPi.GPIO as GPIO
import time
import os
import subprocess
import supervisor
# Définir le numéro du GPIO pour le bouton
BOUTON_GPIO = 18
# Initialiser GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(BOUTON_GPIO, GPIO.IN) # On met en pull-down puisque
# Lorsque l'aimant est placé, la broche est connectée à la masse, tirant ainsi l'entrée vers un niveau logique bas.
# Lorsque l'aimant est retiré, l'entrée est tirée vers le haut à un niveau logique haut.
# Fonction à appeler lors de l'interruption du bouton
def bouton_interruption(channel):
    print('interrupt ok')
    #command = ['ros2', 'run', 'robotix', 'motor']
    #process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    #os.system("python3 /home/robotix/ros2_ws/src/supervisor.py") # Ici, il faut lancer le démarrage de la séquence
    supervisor.run_nodes()
# Ajouter une interruption pour le bouton
#GPIO.add_event_detect(BOUTON_GPIO, GPIO.RISING, callback=bouton_interruption, bouncetime=300) # Vu l condig en pull-up, c'est une détection de front montant
pin_value = 0
try:
    while not GPIO.input(18):
        print(GPIO.input(18))
        time.sleep(1)
    print("I run nodes")
    supervisor.run_nodes()
except KeyboardInterrupt:
    GPIO.cleanup()
