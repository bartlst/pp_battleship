import socket
import json
import threading
import pickle
from _thread import *

HEADER = 64
#IPADDR = socket.gethostbyname(socket.gethostname())
IPADDR = '88.220.118.173'
CONFIG = json.load(open('config.json'))
FORMAT = 'utf-8'
DISCONNECTED_MSG = '!DISCONNECTED'

playersList = []
socketInterface = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketInterface.bind((IPADDR, CONFIG["port"]))


def threaded_client(conn, addr):
    """Function is responsible for connecting client to server, receiving information form client and sending
    information to the client """
    # TODO when client is connected add this player to list of players

    print(f"[New Connection] {addr} connected")

    connected = True

    #conn.send(str.encode("Connected"))

    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = pickle.loads(conn.recv(msg_length))
            if msg == DISCONNECTED_MSG:
                connected = False
            print(f"[{addr}] {msg}")
    conn.close()


# Function is waiting for players to join the lobby and set ready state, if all players are ready for 5 sec
# then game will start
# TODO lobby
# TODO global variables that will present state of game (lobby, game, end)
# when server status is lobby we need information form players about theirs status (ready/not ready) and we will be
# sending information to player about others players status; when all players well be ready for 5s then actual game will
# start
# when server status is game we need information form players about theirs actions ( relocation of battleship, attack
# to another position, and information when player end's his round

def serverStart():
    print("[Server Started] Waiting for connection...")
    socketInterface.listen()
    while True:
        conn, addr = socketInterface.accept()
        thread = threading.Thread(target=threaded_client, args=(conn, addr))
        thread.start()

serverStart()