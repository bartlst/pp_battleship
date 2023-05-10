import network
import threading
import classes
import os

# type of message
DISCONNECTED_MSG = '!DISCONNECTED'
CONNECTING_MSG = '!CONNECTING'
SENDING_MAP_MSG = '!SEND_MAP'
ATTACK_MSG = '!ATTACK'
READINESS_MSG = '!READINESS_STATE'
BATTLESHIP_PUL_MSG = '!BATTLESHIP_PUL'
TIME_LEFT_MSG = '!TIME'
SERVER_INFO_MSG = '!SERVER_INFO'
LOBBY_INFO_MSG = '!LOBBY_INFO'
GAME_INFO_MSG = '!GAME_INFO'


class GAME:
    def __init__(self):
        self.connected = False
        self.network_communication = None
        self.__game_state = 0

        self.__SERVER_game_state
        self.__SERVER_playmaker
        self.__SERVER_players_list

    def connect_to_server(self, server_ip, player_nick):
        """Method is responsible for connecting to the server which have given ip address,
         and after successful connecting method is sending given nickname. Returns True when after successful connecting
          and False when player has not connected to the server"""
        try:
            self.network_connection = network.Network(server_ip)
            message = classes.communication(CONNECTING_MSG, player_nick)
            self.network_connection.send(message)
            self.connected = True
            return True
        except:
            return False

    def quit_game(self):
        """"Method is responsible for sending information to the server with information that player leve the game"""
        message = classes.communication(DISCONNECTED_MSG, False)
        self.network_connection.send(message)

    def __handle_server_messages(self):
        """Method is responsible for receiving information from the server,
        and it is also saving them in private variables"""
        if self.connected:
            message_type = self.network_connection.received_msg.packet_type
            message_data = self.network_connection.received_msg.data

            if message_type == SERVER_INFO_MSG:
                pass
                self.SERVER_game_state
                self.SERVER_playmaker
                self.SERVER_players_list

                # TODO inform user when SERVER_game_state has been changed
            if message_type == LOBBY_INFO_MSG:
                pass
                self.SERVER_lobby_list
                # TODO list of object {player.nick,player.readiness}

            elif message_type == GAME_INFO_MSG:
                pass

            elif message_type == BATTLESHIP_PUL_MSG:
                pass

    def get_server_game_state(self): return self.__SERVER_game_state



def start():
    game = GAME()

    while not game.connected:
        server_ip = input("Input server ip address: ")
        player_nick = input("Input nickname: ")
        game.connect_to_server(server_ip, player_nick)

    while True:
        if game.get_server_game_state() == 0:
            # TODO LOBBY
            #  1. Print list of players with information obout readiness state
            #  2. When everyone is ready print time left
            #  3. Allow player to change his readiness state
            pass
        elif game.get_server_game_state() == 1:
            # TODO preparation room
            #  1. print player map
            #  2. print bellow list of available ships
            #  3. allow to pick one battleship and set coordinates to put it on the map
            #  4. update map after each action
            #  5. allow to sent information with map to the server
            #  6. display time left
            pass
        elif game.get_server_game_state() == 2:
            # TODO war room
            #  1. print player map
            #  2. print enemy players map
            #  3. allow to pick coordinates on enemy player map that player want to attack
            #  4. allow to sent information with attack to the server
            #  5. display playmaker nick
            #  6. display time left
            pass
        elif game.get_server_game_state() == 3:
            # TODO finish
            #  display score table
            pass



os.system('cls')
