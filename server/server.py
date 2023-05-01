import socket
import json
import threading
import pickle
import classes
from _thread import *


class Player:
    def __init__(self, nick):
        self.nick = nick
        self.map = None


HEADER = 64
IPADDR = socket.gethostbyname(socket.gethostname())
CONFIG = json.load(open('config.json'))
FORMAT = 'utf-8'
PORT = 5550

#type of message
DISCONNECTED_MSG = '!DISCONNECTED'
CONNECTING_MSG = '!CONNECTING'
SENDING_MAP_MSG = '!SEND_MAP'
ATTACK_MSG = '!ATTACK'

GAME_STATE = 0
#0 - lobby (server waiting for players)
#1 - setting up the map (server waiting for players to send thier maps)
#3 - game is running (players can send attack actions)

playersList = []
socketInterface = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketInterface.bind((IPADDR, PORT))


def threaded_client(conn, addr):
    """Function is responsible for connecting client to server, receiving information form client and sending
    information to the client """
    # TODO when client is connected add this player to list of players

    print(f"[New Connection] {addr} connected")
    player = None
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length)
            msg = pickle.loads(msg)
            print(f"[{addr[0]}] {msg.packet_type}")

            if msg.packet_type == CONNECTING_MSG and player==None:
                player = Player(msg.data)
                playersList.append(player)
                for p in playersList:
                    print(p.nick)
                print(f"From {addr[0]} player {player.nick} connected!")

            elif msg.packet_type == DISCONNECTED_MSG:
                connected = False
                playersList.remove(player)

            elif msg.packet_type == SENDING_MAP_MSG:
                print(f"Player {player.nick} send a map")
                player.map = msg.data

            elif msg.packet_type == ATTACK_MSG:
                print(f"Player {player.nick} attacked position {msg.data['position'].x, msg.data['position'].y} on "
                      f"{msg.data['attackedPlayer']}'s map")
                for player in playersList:
                    if player.nick == msg.data['attackedPlayer']:
                        if player.map.attacOnPosition(msg.data['position'], 1):
                            print("Trafiony!")
                        else:
                            print("Pudło!")
                        break
    conn.close()

def threaded_game():
    if GAME_STATE == 0:

    elif GAME_STATE == 1:

    elif GAME_STATE == 2:

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