import socket
import sys


class Client():
    def __init__(self, host):
        super(Client, self).__init__()
        self.host = host
        self.port = 65535

        # Create a socket (SOCK_STREAM means a TCP socket)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return

    def init(self):
        # Connect to server and send data
        self.sock.settimeout(5)
        self.sock.connect((self.host, self.port))
        self.sock.send("init".encode('utf-8'))
        response = bytes.decode(self.sock.recv(1024))
        return str(response)

    def live(self):
        pass
