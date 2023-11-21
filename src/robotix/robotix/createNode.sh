#!/bin/bash

# Vérifie s'il y a trois arguments en entrée
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <nom_de_fichier> <nom_du_node> <nom_de_la_classe>"
    exit 1
fi

# Récupère les arguments en entrée
filename="$1"
node_name="$2"
class_name="$3"

# Crée le fichier avec la commande touch
echo "Création du fichier $filename"
touch "$filename"

# Donne les droits d'exécution au fichier
echo "Donne les droits d'exécution à $filename"
chmod 777 "$filename"

# Ajoute les lignes Python dans le fichier
echo -e "#!/usr/bin/env python3\nimport rclpy\nfrom rclpy.node import Node\nfrom geometry_msgs.msg import Twist\nfrom std_msgs.msg import Int16\nclass $class_name(Node):\n\n    def __init__(self):\n        super().__init__(\"$node_name\")\n        self.publisher_ = self.create_publisher(Twist, \"/robotix/topic\", 10)\n        self.subscriber_ = self.create_subscription(Twist, \"/robotix/topic\", self.my_callback, 10)\n        self.timer_ = self.create_timer(0.5, self.my_publish)\n        self.get_logger().info(\"Hello from $node_name\")\n\n    def my_callback(self):\n        pass\n\n    def my_publish(self):\n        pass\n\ndef main(args=None):\n    rclpy.init(args=args)\n    node = $class_name()\n    rclpy.spin(node)\n    rclpy.shutdown()\n\nif __name__ == '__main__':\n    main()" > "$filename"

echo "Le fichier $filename a été créé avec succès et les lignes ont été ajoutées."
