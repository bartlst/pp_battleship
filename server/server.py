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

# type of message [This will be put in header parameter in communication class]
DISCONNECTED_MSG = '!DISCONNECTED'
CONNECTING_MSG = '!CONNECTING'
SENDING_MAP_MSG = '!SEND_MAP'
ATTACK_MSG = '!ATTACK'
READINESS_MSG = '!READINESS_STATE'
BATTLESHIP_PUL_MSG = '!BATTLESHIP_PUL'
TIME_LEFT_MSG = '!TIME'
LOBBY_INFO_MSG = '!LOBBY_INFO'
GAME_INFO_MSG = '!GAME_INFO'

GAME_STATE = 0
# 0 - lobby (server waiting for players)
# 1 - setting up the map (server waiting for players to send theirs maps)
# 2 - game is running (players can send attack actions)
PLAYMAKER = None  # variable that stores object player, when round belongs to player variable is storing this player
ROUND_FINISHED = False  # when playmaker sent message "round finished" will be set on True and on next round
# variable will be set on False
playersList = []
socketInterface = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketInterface.bind((IPADDR, PORT))


def threaded_client(conn, addr):
    """Function is responsible for connecting client to server, receiving information form client"""
    global ROUND_FINISHED

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
                ROUND_FINISHED = True
                for player in playersList:
                    if player.nick == msg.data['attackedPlayer']:
                        if player.map.attacOnPosition(msg.data['position'], 1):
                            print("Trafiony!")
                        else:
                            print("Pudło!")
                        break
    conn.close()


def threaded_game():
    """Function that is responsible for game logic, function is basing on global variables."""
    # importing global variables
    global GAME_STATE
    global PLAYMAKER
    global ROUND_FINISHED

    # main loop
    while True:
        # LOBBY STATE
        if GAME_STATE == 0:
            ready_players = 0
            player_readiness_list = []
            for player in playersList:
                if player.readiness:
                    ready_players += 1
                else:
                    ready_players -= 1
                temp_dict = {"player": player.nick, "Readiness": player.readiness}
                player_readiness_list.append(temp_dict)
            message_to_all = classes.communication(READINESS_MSG, player_readiness_list)
            send_msg_to_all(message_to_all)
            if ready_players == len(playersList) and len(playersList) > 1:
                print(f"All {ready_players} players are ready!")
                if (round(time.time())-player_readiness_time) >= 5:
                    GAME_STATE = 1
                    print("GAME IS STARTING...")
                    starting_state_1_time = round(time.time())
            else:
                player_readiness_time = round(time.time())
        # PREPARATION ROOM
        elif GAME_STATE == 1:
            temp_dict = {"map_width": CONFIG["map_width"],
                         "map_height": CONFIG["map_height"],
                         "battleship_pul": battleships.battleships_pul}
            message = classes.communication(BATTLESHIP_PUL_MSG, temp_dict)
            #send_msg_to_all(message)

            time_limit_in_min = 0.5
            time_left = (starting_state_1_time + 60 * time_limit_in_min - round(time.time())) / 60
            all_maps_received = True
            for player in playersList:
                if not player.map:
                    all_maps_received = False
                    break
            if all_maps_received or time_left <= 0:
                print("All maps received")
                if not all_maps_received:
                    for player in playersList:
                        if not player.map:
                            player.map = classes.Map(CONFIG["map_width"], CONFIG["map_height"])
                            position = classes.Position(0, 0)
                            for ships in battleships.battleships_pul:
                                temp_battleship = ships
                                player.map.putBattleship(position, "horizontal", temp_battleship)
                                position.x += 1

                for player in playersList:
                    print(f"{player.nick}'s map")
                    for row in player.map.map:
                        print_row = ""
                        for position in row:
                            if position['battleship']:
                                print_row += "[X]"
                            else:
                                print_row += "[.]"
                        print(print_row)
                GAME_STATE = 2
                PLAYMAKER = playersList[0]
                round_time_start = round(time.time())


            #print(time_left)
            #message = classes.communication(TIME_LEFT_MSG, time_left)
            #send_msg_to_all(message)
        # WAR [GAME IS RUNNING]
        elif GAME_STATE == 2:
            # TODO for each player check if health of all battleships is equal to 0, if it is game is over
            #  for this player, if there is only one player left he will be set as winner and game will ends.
            round_time = CONFIG["round_time_min"] * 60
            if round(time.time()) >= round_time_start + round_time or ROUND_FINISHED:
                playmaker_index = playersList.index(PLAYMAKER)
                if playersList[playmaker_index+1] == len(playersList):
                    PLAYMAKER = playersList[0]
                else:
                    PLAYMAKER = playersList[playmaker_index+1]
                print(f'New playmaker {PLAYMAKER.nick}')
                round_time_start = round(time.time())
                ROUND_FINISHED = False

        # GLOBAL MESSAGE THAT WILL BE SENT FOR EACH TIME
        # [Players list] [Game state] [Playmaker info] [Time]
        send_msg_to_all
        # TODO for each time sent to all players game state


def send_msg_to_all(data):
    """Function is responsible for sending message to all players"""
    for player in playersList:
        message = pickle.dumps(data)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        player.connection_chanel.send(send_length)
        player.connection_chanel.send(message)


def send_msg(player, data):
    """"Function is responsible for sending message to given player"""
    message = pickle.dumps(data)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    player.connection_chanel.send(send_length)
    player.connection_chanel.send(message)


def server_start():
    """"Main function that is responsible for server, listening for new connections, starting threads for new clients
    and also running one thread that is responsible for game logic"""
    print("[Server Started] Waiting for connection...")
    socketInterface.listen()
    game_thread = threading.Thread(target=threaded_game)
    game_thread.start()
    while True:
        conn, addr = socketInterface.accept()
        player_thread = threading.Thread(target=threaded_client, args=(conn, addr))
        player_thread.start()


server_start()