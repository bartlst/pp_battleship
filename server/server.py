import socket
import json
import threading
import pickle
import time
import classes
import battleships
import time

# TODO add description to each function/method
# TODO add comments
class Player:
    def __init__(self, nick, connection_chanel):
        self.nick = nick
        self.connection_chanel = connection_chanel
        self.map = None
        self.readiness = False
        self.active = True


HEADER = 64
IPADDR = socket.gethostbyname(socket.gethostname())
CONFIG = json.load(open('config.json'))
FORMAT = 'utf-8'
PORT = 5550
ROUND_FINISHED = False

#type of message
DISCONNECTED_MSG = '!DISCONNECTED'
CONNECTING_MSG = '!CONNECTING'
SENDING_MAP_MSG = '!SEND_MAP'
ATTACK_MSG = '!ATTACK'
READINESS_MSG = '!READINESS_STATE'
PREPARATION_ROOM_MSG = '!PREPARATION_ROOM_INFO'
TIME_LEFT_MSG = '!TIME'
SERVER_INFO_MSG = '!SERVER_INFO'
LOBBY_INFO_MSG = '!LOBBY_INFO'
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
    global ROUND_FINISHED
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length)
            msg = pickle.loads(msg)
            print(f"[{addr[0]}] {msg.packet_type}")
            print("PLAYMAKER:", PLAYMAKER)
            print(GAME_STATE == 2)

            if msg.packet_type == CONNECTING_MSG and player == None and GAME_STATE == 0:
                player = Player(msg.data, conn)
                playersList.append(player)
                for p in playersList:
                    print(p.nick)
                print(f"From {addr[0]} player {player.nick} connected!")
                print

            elif msg.packet_type == DISCONNECTED_MSG:
                connected = False
                playersList.remove(player)

            elif msg.packet_type == READINESS_MSG:
                if player.readiness:
                    print(f"Player {player.nick} is not ready to play")
                    player.readiness = False
                else:
                    print(f"Player {player.nick} is ready to play")
                    player.readiness = True
            elif msg.packet_type == SENDING_MAP_MSG:
                print(f"Player {player.nick} send a map")
                player.map = msg.data

            elif msg.packet_type == ATTACK_MSG and GAME_STATE == 2:
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
    global GAME_STATE
    global PLAYMAKER
    global ROUND_FINISHED

    while True:
        time.sleep(0.5)
        if GAME_STATE == 0:
            ready_players = 0
            player_readiness_list = []

            for player in playersList:
                if player.readiness:
                    ready_players += 1
                else:
                    ready_players -= 1
                temp_dict = {"nick": player.nick, "readiness": player.readiness}
                player_readiness_list.append(temp_dict)

            if ready_players == len(playersList) and len(playersList) > 1:
                print(f"All {ready_players} players are ready!")
                if (round(time.time())-player_readiness_time) >= 10:
                    GAME_STATE = 1
                    print("GAME IS STARTING...")
                    starting_state_1_time = round(time.time())
            else:
                player_readiness_time = round(time.time())
            lobby_time = round(time.time()) - player_readiness_time
            message_data = {"player_list": player_readiness_list, "time": lobby_time}
            message = classes.communication(LOBBY_INFO_MSG, message_data)
            send_msg_to_all(message)

        elif GAME_STATE == 1:
            time_limit_in_min = CONFIG["preparation_room_time_min"]
            time_left = round((starting_state_1_time + 60 * time_limit_in_min - round(time.time())) / 60, 1)
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
                                print_row += "[ ]"
                        print(print_row)
                GAME_STATE = 2
                round_time_left = round(time.time())
                PLAYMAKER = playersList[0]
            message_data = {"map_width": CONFIG["map_width"],
                            "map_height": CONFIG["map_height"],
                            "battleship_pul": battleships.battleships_pul,
                            "time_left": time_left}
            message = classes.communication(PREPARATION_ROOM_MSG, message_data)
            send_msg_to_all(message)

        elif GAME_STATE == 2:
            round_time_limit = CONFIG["round_time_min"]
            time_left = round((round_time_left + 60 * round_time_limit - round(time.time())) / 60, 1)
            active_players = []
            #print(time_left)
            for player in playersList:
                if player.map.battleships_hp() <= 0:
                    player.active = False
                else:
                    active_players.append(player)

            for player in active_players:
                enemy_players = []
                playmaker_info = False
                if PLAYMAKER == player:
                    playmaker_info = True
                for enemy in active_players:
                    if enemy != player:
                        enemy_data = {"nick": enemy.nick, "enemy_map": enemy.map.get_blank_map()}
                        enemy_players.append(enemy_data)
                message_data = {
                    "enemy_players": enemy_players,
                    "if_playmaker": playmaker_info,
                    "time_left": time_left,
                    "map": player.map
                }
                message = classes.communication(GAME_INFO_MSG, message_data)
                send_msg(player, message)

            if time_left <= 0 or ROUND_FINISHED:
                playmaker_index = playersList.index(PLAYMAKER)
                if playmaker_index == (len(playersList)-1):
                    PLAYMAKER = playersList[0]
                else:
                    PLAYMAKER = playersList[playmaker_index + 1]
                print(f'New playmaker {PLAYMAKER.nick}')
                round_time_left = round(time.time())
                ROUND_FINISHED = False

        # TODO for each time sent to all players game state
        message_data = {
            "game_state": GAME_STATE,
        }
        messages = classes.communication(SERVER_INFO_MSG, message_data)
        send_msg_to_all(messages)


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