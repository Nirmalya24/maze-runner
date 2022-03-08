import socket
import sys

from config import *


class ClientSocket(socket.socket):
    def __init__(self):
        super(ClientSocket, self).__init__(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        try: 
            super(ClientSocket, self).connect((SERVER_IP, SERVER_PORT))
        except:
            print("Cannot connect to server. Goodbye!")
            sys.exit(0)

    def recv_data(self):
        try:
            return self.recv(512).decode('utf-8')
        except:
            print("Cannot receive data from server. Goodbye!")

    def send_data(self, message):
        try:
            return self.send(message.encode('utf-8'))
        except Exception as e:
            print("Cannot send data to server. Goodbye!")

    def exit(self):
        self.close()
        sys.exit(0)
