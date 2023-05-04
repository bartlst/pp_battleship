import socket
import json
import threading
import pickle
import time
import classes
import battleships

# TODO add description to each function/method
# TODO add comments
class Player:
    def __init__(self, nick, connection_chanel):
        self.nick = nick
        self.connection_chanel = connection_chanel
        self.map = None
        self.readiness = False


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
READINESS_MSG = '!READINESS_STATE'
BATTLESHIP_PUL_MSG = '!BATTLESHIP_PUL'
TIME_LEFT_MSG = '!TIME'
GAME_INFO_MSG = '!GAME_INFO'

GAME_STATE = 0
#0 - lobby (server waiting for players)
#1 - setting up the map (server waiting for players to send thier maps)
#2 - game is running (players can send attack actions)
PLAYMAKER = None
playersList = []
socketInterface = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketInterface.bind((IPADDR, PORT))


def threaded_client(conn, addr):
    """Function is responsible for connecting client to server, receiving information form client and sending
    information to the client """


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

            if msg.packet_type == CONNECTING_MSG and player == None and GAME_STATE == 0:
                player = Player(msg.data, conn)
                playersList.append(player)
                for p in playersList:
                    print(p.nick)
                print(f"From {addr[0]} player {player.nick} connected!")

            elif msg.packet_type == DISCONNECTED_MSG:
                connected = False
                playersList.remove(player)

            elif msg.packet_type == READINESS_MSG:
                player.readiness = msg.data
                if player.readiness:
                    print(f"Player {player.nick} is ready to play")
                else:
                    print(f"Player {player.nick} is not ready to play")
            elif msg.packet_type == SENDING_MAP_MSG:
                print(f"Player {player.nick} send a map")
                player.map = msg.data

            elif msg.packet_type == ATTACK_MSG and PLAYMAKER == player and GAME_STATE == 2:
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
    global GAME_STATE
    while True:
        if GAME_STATE == 0:
            ready_players = 0
            player_readiness_list = []
            for player in playersList:
                if player.readiness:
                    ready_players += 1
                else:
                    ready_players -= 1
                temp_dict = {"player":player.nick, "Readiness": player.readiness}
                player_readiness_list.append(temp_dict)
            message = classes.communication(READINESS_MSG, player_readiness_list)
            send_msg_to_all(message)
            if ready_players == len(playersList) and len(playersList) > 1:
                print(f"All {ready_players} players are ready!")
                if (round(time.time())-player_readiness_time) >= 5:
                    GAME_STATE = 1
                    print("GAME IS STARTING...")
                    starting_state_1_time = round(time.time())
            else:
                player_readiness_time = round(time.time())

        elif GAME_STATE == 1:
            # TODO test message with array of battleships
            message = classes.communication(BATTLESHIP_PUL_MSG, battleships.battleships_pul)
            send_msg_to_all(message)

            time_limit_in_min = 1
            time_left = (starting_state_1_time + 60 * time_limit_in_min - round(time.time())) / 60
            all_maps_received = True
            for player in playersList:
                if not player.map:
                    all_maps_received = False
                    break
            if all_maps_received or time_left <= 0:
                print("All maps received")
                if not all_maps_received:
                    # TODO set a map with all battleships on it and assign to player without a map
                    #  ( all battleship in one row)
                    pass
                break

            print(time_left)
            message = classes.communication(TIME_LEFT_MSG, time_left)
            send_msg_to_all(message)

        elif GAME_STATE == 2:
            print(GAME_STATE)

        # TODO for each time sent to all players game state

def send_msg_to_all(data):
    for player in playersList:
        message = pickle.dumps(data)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        player.connection_chanel.send(send_length)
        player.connection_chanel.send(message)
def send_msg(player, data):
    message = pickle.dumps(data)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    player.connection_chanel.send(send_length)
    player.connection_chanel.send(message)



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
    game_thread = threading.Thread(target=threaded_game)
    game_thread.start()
    while True:
        conn, addr = socketInterface.accept()
        player_thread = threading.Thread(target=threaded_client, args=(conn, addr))
        player_thread.start()

serverStart()