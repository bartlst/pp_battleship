import socket
import pickle
import classes

DISCONNECTED_MSG = '!DISCONNECTED'
CONNECTING_MSG = '!CONNECTING'
SENDING_MAP_MSG = '!SEND_MAP'
ATTACK_MSG = '!ATTACK'


HEADER = 64
#SERVERIP = "192.168.68.105"
SERVERIP = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'
DISCONNECTED_MSG = '!DISCONNECTED'
PORT = 5550

# TODO create a class that will be containing all of needed information about game that client will be sending to server
class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = (SERVERIP, PORT)
        self.client.connect(self.addr)
    
    def send(self, data):

        message = pickle.dumps(data)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        self.client.send(send_length)
        self.client.send(message)

    def recive(self):
        pass



# TODO check len of information and send to server
# TODO pickle the information and send it to server

battleshipOne = classes.Battleship(54, 0, 0, 3, 1)
mapOne = classes.Map(10, 10)
position = classes.Position(2, 2)

mapOne.putBattleship(position, "horizontal", battleshipOne)
n = Network()




nickName = input("Wprowadz swoj nick: ")

msg = classes.communication(CONNECTING_MSG, nickName)
n.send(msg)
msg = classes.communication(SENDING_MAP_MSG, mapOne)
n.send(msg)
x = input()
if x == "":
    dic = {
        "position": position,
        "attackedPlayer": "Alfred"
    }
    msg = classes.communication(ATTACK_MSG, dic)
    n.send(msg)
x = input("czekej")