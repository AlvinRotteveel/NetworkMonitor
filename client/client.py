import socket
import threading
import pickle


def threaded(fn):
    def wrapper(*args, **kwargs):
        threading.Thread(target=fn, args=args, kwargs=kwargs).start()
    return wrapper


class Client():

    def connect(self, host):
        self.host = host
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, 1234))
        return sock

    def send(self, command):
        sock = self.connect(self.host)
        data = True
        recv_data = []

        sock.sendall(command.encode('utf-8'))

        while data:
            data = sock.recv(10240)
            try:
                recv_data = pickle.loads(data)
            except EOFError:
                break

        sock.close()
        return recv_data