import socket
import pickle
import classes
import threading

#type of message
DISCONNECTED_MSG = '!DISCONNECTED'
CONNECTING_MSG = '!CONNECTING'
SENDING_MAP_MSG = '!SEND_MAP'
ATTACK_MSG = '!ATTACK'
READINESS_MSG = '!READINESS_STATE'
BATTLESHIP_PUL_MSG = '!BATTLESHIP_PUL'
TIME_LEFT_MSG = '!TIME'
GAME_INFO_MSG = '!GAME_INFO'



HEADER = 64
FORMAT = 'utf-8'
DISCONNECTED_MSG = '!DISCONNECTED'
PORT = 5550
# TODO add description to each function/method
# TODO add comments


class Network:
    def __init__(self, server_ip):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = (server_ip, PORT)
        self.client.connect(self.addr)
        receive_thread = threading.Thread(target=self.__receive_msg)
        receive_thread.start()
        self.received_msg = None


    def send(self, data):

        message = pickle.dumps(data)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        self.client.send(send_length)
        self.client.send(message)

    def __receive_msg(self):
        print("receiving ON")
        while True:
            msg_length = self.client.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = self.client.recv(msg_length)
                msg = pickle.loads(msg)
                self.received_msg = msg






# battleshipOne = classes.Battleship(54, 0, 0, 1, 1)
# mapOne = classes.Map(10, 10)
# position = classes.Position(9, 9)
#
# mapOne.putBattleship(position, "horizontal", battleshipOne)
# n = Network()
#
#
#
#
# nickName = input("Wprowadz swoj nick: ")
#
# msg = classes.communication(CONNECTING_MSG, nickName)
# n.send(msg)
# x = input("Ready")
# msg = classes.communication(READINESS_MSG, True)
# n.send(msg)
# x = input("Map")
# msg = classes.communication(SENDING_MAP_MSG, mapOne)
# n.send(msg)
#
# x = input("Attack")
# position = classes.Position(0, 0)
# temp_dict = {"attackedPlayer": "bolek", "position": position}
# msg = classes.communication(ATTACK_MSG, temp_dict)
# n.send(msg)



