import subprocess
import time

def run_node(command):
    """Exécute un noeud et le relance en cas d'arrêt inattendu."""
    while True:
        print(f"Démarrage du noeud avec la commande : {' '.join(command)}")
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        
        try:
            output = ""
            while True:
                line = process.stdout.readline()
                if line == '' and process.poll() is not None:
                    break
                if line:
                    print(line.strip())
                    output += line
        except KeyboardInterrupt:
            print("\nArrêt demandé par l'utilisateur.")
            process.terminate()
            break

        # Vérifiez la sortie complète pour une erreur spécifique
        if "ExternalShutdownException" in output:
            print("Relancement du noeud en raison d'une condition d'erreur spécifique...")
        else:
            print("Le noeud s'est terminé normalement ou en raison d'une autre erreur, il ne sera pas relancé.")
            break

        time.sleep(1)  # Un court délai avant de relancer


def run_nodes():
    """Lance et gère plusieurs noeuds, en s'assurant de relancer le noeud A si nécessaire."""
    # Commandes pour lancer vos noeuds ROS 2
    node_ctrl_nav_command = ['ros2', 'run', 'robotix', 'ctrl_nav']
    node_motor_command = ['ros2', 'run', 'robotix', 'motor']

    # Lancer le noeud B dans un processus séparé sans surveillance spéciale
    print("Démarrage du noeud B...")
    #node_motor_process = subprocess.Popen(node_motor_command)

    # Gérer et potentiellement relancer le noeud A
    run_node(node_ctrl_nav_command)

    # Nettoyage: Assurez-vous que le noeud B est également arrêté lorsque le script se termine
   # node_motor_process.terminate()
   # try:
        #node_motor_process.wait(timeout=5)
   # except subprocess.TimeoutExpired:
        #node_motor_process.kill()

if __name__ == '__main__':
    run_nodes()

