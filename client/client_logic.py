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
GAME_INFO_MSG = '!GAME_INFO'


def game():
    connected = False
    while not connected:
        try:
            server_ip = input("Input server ip address: ")
            network_connection = network.Network(server_ip)
            connected = True
            player_nick = input("Input your nickname: ")
            message = classes.communication(CONNECTING_MSG, player_nick)
            network_connection.send(message)
        except:
            print("[Failed to connect to the server] "
                  "\nCheck your network connection and make sure the ip address you entered is correct")
            input()
    game_is_running = True

    while game_is_running:
        print(network_connection.received_msg)
        # for each game state different actions
        # lobby: possibility to change readiness, receive player list and print it
        # preparation room: create a map base on given variables,
        # create array of battleships base on given data from server
        # war: print maps, and round time (create a map for each enemy and mark on that where you shot (hit or miss)
        # when player is a playmaker give him possibility to create a possition class which will be sent
        # to server on the end of round
        # on the beginning of each loop read received msg and write data form msg to local variables
        # console clear function


game()