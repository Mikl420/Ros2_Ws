# Notes : Connecter le capteur de démarrage à la broche 18 du Raspberry Pi, brancher l'autre côté à la masse.
import RPi.GPIO as GPIO
import time
import os
# Définir le numéro du GPIO pour le bouton
BOUTON_GPIO = 18
# Initialiser GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(BOUTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # On met en pull-down puisque 
# Lorsque l'aimant est placé, la broche est connectée à la masse, tirant ainsi l'entrée vers un niveau logique bas.
# Lorsque l'aimant est retiré, l'entrée est tirée vers le haut à un niveau logique haut. 
# Fonction à appeler lors de l'interruption du bouton
def bouton_interruption(channel):
    print('interrupt ok')
    os.system("sudo python3 supervisor.py") # Ici, il faut lancer le démarrage de la séquence
# Ajouter une interruption pour le bouton
GPIO.add_event_detect(BOUTON_GPIO, GPIO.RISING, callback=bouton_interruption, bouncetime=300) # Vu l condig en pull-up, c'est une détection de front montant
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
