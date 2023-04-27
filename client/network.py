import socket
import pickle
import classes

#
HEADER = 64
SERVERIP = "192.168.0.37"
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

p = classes.Position(5, 5)
n = Network()


n.send("hello")
n.send(DISCONNECTED_MSG)

