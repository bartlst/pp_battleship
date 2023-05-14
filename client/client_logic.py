import network
import threading
import classes
import os
import time

# type of message
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


class GAME:
    def __init__(self):
        self.connected = False
        self.network_communication = None
        self.__game_state = 0

        self.__SERVER_info = None
        self.__SERVER_lobby = None
        self.__SERVER_game_info = None
        self.__SERVER_preparation_room = None

        self.__user_input = None
        self.user_map = None
        self.user_battleship_pull = []

    def connect_to_server(self, server_ip, player_nick):
        """Method is responsible for connecting to the server which have given ip address,
         and after successful connecting method is sending given nickname. Returns True when after successful connecting
          and False when player has not connected to the server"""
        try:
            self.network_communication = network.Network(server_ip)
            message = classes.communication(CONNECTING_MSG, player_nick)
            self.network_communication.send(message)
            self.connected = True

            receiving_thread = threading.Thread(target=self.__handle_server_messages)
            receiving_thread.start()
            return True
        except:
            return False

    def quit_game(self):
        """"Method is responsible for sending information to the server with information that player leve the game"""
        message = classes.communication(DISCONNECTED_MSG, False)
        self.network_communication.send(message)

    def __handle_server_messages(self):
        """Method is responsible for receiving information from the server,
        and it is also saving them in private variables"""
        while self.connected:
            message = self.network_communication.receiving()
            if message:
                message_type = message.packet_type
                message_data = message.data
                if message_type == SERVER_INFO_MSG:
                    self.__SERVER_info = message_data

                if message_type == LOBBY_INFO_MSG:
                    self.__SERVER_lobby = message_data

                elif message_type == GAME_INFO_MSG:
                    self.__SERVER_game_info = message_data

                elif message_type == PREPARATION_ROOM_MSG:
                    self.__SERVER_preparation_room = message_data

    def get_server_data(self):
        directory = {
            "SERVER_info": self.__SERVER_info,
            "SERVER_lobby": self.__SERVER_lobby,
            "SERVER_game_info": self.__SERVER_game_info,
            "SERVER_preparation_room_info": self.__SERVER_preparation_room,
        }

        return directory

    def user_input_function(self):
        while True:
            temp_input = input()
            self.__user_input = temp_input

    def reset_input(self):
        self.__user_input = None

    def get_user_input(self):
        return self.__user_input

    def set_preparation_room(self, config):
        self.user_battleship_pull = config["battleship_pul"]
        self.user_map = classes.Map(config["map_width"], config["map_height"])

    def set_map(self, map):
        self.user_map = map

    def get_user_map(self):
        return self.user_map

    def get_battleship_pull(self):
        return self.user_battleship_pull


def printable_map(map):
    map_string = ""
    for row in map:
        row_print = ""
        for position in row:
            if position['occupied'] and position['attacked']:
                row_print += "[~]"
            elif position['occupied']:
                row_print += "[X]"
            elif position['attacked']:
                row_print += "[@]"
            else:
                row_print += "[ ]"
        map_string += row_print + "\n"
    return map_string


def start():
    game = GAME()
    display = None
    while not game.connected:
        server_ip = input("Input server ip address: ")
        player_nick = input("Input nickname: ")
        game.connect_to_server(server_ip, player_nick)

    thread_input = threading.Thread(target=game.user_input_function)
    thread_input.start()

    while True:
        server_data = game.get_server_data()
        if server_data["SERVER_info"]:

            if server_data["SERVER_info"]["game_state"] == 0:
                if display != server_data["SERVER_lobby"]:
                    os.system('cls')
                    print("[LOBBY]")
                    for player in server_data["SERVER_lobby"]["player_list"]:
                         print(f"Player: {player['nick']} \t Readiness: {player['readiness']}")
                         display = server_data["SERVER_lobby"]
                    print(f"\nTime: {server_data['SERVER_lobby']['time']}")
                    print("Press ENTER to change readiness state...")
                if isinstance(game.get_user_input(), str):
                    message = classes.communication(READINESS_MSG, None)
                    game.network_communication.send(message)
                    game.reset_input()
            elif server_data["SERVER_info"]["game_state"] == 1:
                os.system('cls')
                print("[PREPARATION ROOM]")
                if server_data['SERVER_preparation_room_info']:
                    print(f"\n[TIME LEFT: {server_data['SERVER_preparation_room_info']['time_left']}]")
                    #print(server_data["SERVER_preparation_room_info"])

                    if game.get_user_map():
                        if len(game.user_battleship_pull) == 0:
                            message_data = game.user_map
                            message = classes.communication(SENDING_MAP_MSG, message_data)
                            game.network_communication.send(message)
                            print("[Finished]")
                        else:
                            battleship_index = 0
                            map_to_print = game.get_user_map()
                            print(printable_map(map_to_print.map))

                            print("\n\n[BATTLESHIP PULL]")
                            for battleship in game.get_battleship_pull():
                                print(f"[{battleship_index}]. {battleship.name}")
                                battleship_index += 1

                            print("Pick ship you want to put on map : ")
                            if isinstance(game.get_user_input(), str) and not picked_index:
                                if game.get_user_input().isnumeric():
                                    picked_index = game.get_user_input()
                                    game.reset_input()
                            if picked_index:
                                int_picked_index = int(picked_index)
                                if not len(game.get_battleship_pull()) >= int_picked_index+1 and int_picked_index >= 0:
                                    print("Battleship with this index don't exist")
                                    picked_index = None
                                else:
                                    print(game.get_battleship_pull()[int_picked_index].name)

                                    print("Enter the row number [Y] in which you want to place the ship:")
                                    if isinstance(game.get_user_input(), str) and not picked_y_pos:
                                        if game.get_user_input().isnumeric():
                                            picked_y_pos = game.get_user_input()
                                            game.reset_input()
                                    if picked_y_pos:
                                        int_picked_y_pos = int(picked_y_pos)
                                        if not len(game.get_user_map().map) >= int_picked_y_pos + 1 and int_picked_y_pos >= 0:
                                            print("You have entered an incorrect row number")
                                            picked_y_pos = None
                                        else:
                                            print(f"[POSITION] Y: {picked_y_pos}")

                                            print("Enter the column number [X] in which you want to place the ship:")
                                            if isinstance(game.get_user_input(), str) and not picked_x_pos:
                                                if game.get_user_input().isnumeric():
                                                    picked_x_pos = game.get_user_input()
                                                    game.reset_input()
                                            if picked_x_pos:
                                                int_picked_x_pos = int(picked_x_pos)
                                                if not len(game.get_user_map().map[int_picked_y_pos]) >= int_picked_x_pos + 1 \
                                                        and int_picked_x_pos >= 0:
                                                    print("You have entered an incorrect column number")
                                                    picked_x_pos = None
                                                else:
                                                    print(f"[POSITION] X: {picked_x_pos}")

                                                    print("Pick orientation [0/1]:\n"
                                                          "[0]. Horizontal\n"
                                                          "[1]. Vertical")
                                                    if isinstance(game.get_user_input(), str) and not picked_direction:
                                                        if game.get_user_input().isnumeric():
                                                            picked_direction = game.get_user_input()
                                                            game.reset_input()
                                                    if picked_direction:
                                                        int_picked_direction = int(picked_direction)
                                                        if int_picked_direction == 0:
                                                            picked_direction = "horizontal"
                                                            position_picked = True
                                                        elif int_picked_direction == 1:
                                                            picked_direction = "vertical"
                                                            position_picked = True
                                                        else:
                                                            print("You have entered an incorrect orientation ")
                                                            picked_direction = None

                            if position_picked:
                                picked_battleship = game.get_battleship_pull()[int(picked_index)]
                                picked_position = classes.Position(int(picked_x_pos), int(picked_y_pos))
                                if game.user_map.putBattleship(picked_position, picked_direction, picked_battleship):
                                    print("Success!")
                                    game.user_battleship_pull.pop(int(picked_index))
                                else:
                                    print("Not enough space for a battleship ")

                                picked_direction = None
                                picked_index = None
                                picked_y_pos = None
                                picked_x_pos = None
                                position_picked = False

                    else:
                        picked_direction = None
                        picked_index = None
                        picked_y_pos = None
                        picked_x_pos = None
                        position_picked = False
                        first_round = True
                        game.set_preparation_room(server_data['SERVER_preparation_room_info'])
                    time.sleep(2)
            elif server_data["SERVER_info"]["game_state"] == 2:
                os.system('cls')

                if first_round:
                    print("first_round")
                    picked_player_index = None
                    attack_y_pos = None
                    attack_x_pos = None
                    position_picked = False
                    first_round = False
                    attack_position_picked = False
                print("[WAR!]")
                if server_data['SERVER_game_info']:
                    print(f"PLAYMAKER: {server_data['SERVER_game_info']['if_playmaker']}")
                    print(f"[TIME]: {server_data['SERVER_game_info']['time_left']}")
                    game.user_map = server_data["SERVER_game_info"]["map"]
                    map_to_print = game.get_user_map()
                    print(printable_map(map_to_print.map))

                    for enemy in server_data["SERVER_game_info"]["enemy_players"]:
                        print(f"{enemy['nick']}'s map: \n")
                        print(printable_map(enemy['enemy_map']))

                    if server_data['SERVER_game_info']['if_playmaker']:
                        print("\n\n[ENEMY PLAYERS]")
                        index = 0
                        for enemy in server_data["SERVER_game_info"]["enemy_players"]:
                            print(f"[{index}] {enemy['nick']}")
                            index += 1
                        print("Pick player you want to attack : ")
                        if isinstance(game.get_user_input(), str) and not picked_player_index:
                            if game.get_user_input().isnumeric():
                                picked_player_index = game.get_user_input()
                                game.reset_input()
                        if picked_player_index:
                            int_picked_player_index = int(picked_player_index)
                            if not len(server_data["SERVER_game_info"]["enemy_players"]) >= int_picked_player_index + 1 \
                                    and int_picked_player_index >= 0:
                                print("Player with this index don't exist")
                                picked_player_index = None
                            else:
                                print("Enter the row number [Y]:")
                                if isinstance(game.get_user_input(), str) and not attack_y_pos:
                                    if game.get_user_input().isnumeric():
                                        attack_y_pos = game.get_user_input()
                                        game.reset_input()
                                if attack_y_pos:
                                    int_picked_y_pos = int(attack_y_pos)

                                    if not len(game.get_user_map().map) >= int_picked_y_pos + 1 and int_picked_y_pos >= 0:
                                        print("You have entered an incorrect row number")
                                        attack_y_pos = None
                                    else:
                                        print(f"[POSITION] Y: {attack_y_pos}")

                                        print("Enter the column number [X]:")
                                        if isinstance(game.get_user_input(), str) and not attack_x_pos:
                                            if game.get_user_input().isnumeric():
                                                attack_x_pos = game.get_user_input()
                                                game.reset_input()
                                        if attack_x_pos:
                                            int_picked_x_pos = int(attack_x_pos)
                                            if not len(game.get_user_map().map[int_picked_y_pos]) >= int_picked_x_pos + 1 \
                                                    and int_picked_x_pos >= 0:
                                                print("You have entered an incorrect column number")
                                                attack_x_pos = None
                                            else:
                                                print(f"[POSITION] X: {attack_x_pos}")
                                                attack_position_picked = True
                        if attack_position_picked:
                            attack_position = classes.Position(int(attack_x_pos), int(attack_y_pos))
                            message_data = {
                                "attackedPlayer": server_data["SERVER_game_info"]["enemy_players"]
                                [int(picked_player_index)]["nick"],
                                "position": attack_position
                            }
                            message = classes.communication(ATTACK_MSG, message_data)
                            game.network_communication.send(message)
                            attack_position_picked = False
                            picked_player_index = None
                            attack_y_pos = None
                            attack_x_pos = None
                    else:
                        print("Wait for your turn")


                time.sleep(2)

                # TODO war room
                #  1. print player map
                #  2. print enemy players map
                #  3. allow to pick coordinates on enemy player map that player want to attack
                #  4. allow to sent information with attack to the server
                #  5. display playmaker nick
                #  6. display time left
                pass
            elif server_data["game_state"] == 3:
                # TODO finish
                #  display score table
                pass
            time.sleep(0.5)

start()
