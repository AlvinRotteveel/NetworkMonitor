import socketserver
import pickle
import threading
from agent.database import get_last_packet


def threaded(fn):
    def wrapper(*args, **kwargs):
        threading.Thread(target=fn, args=args, kwargs=kwargs).start()
    return wrapper

class ServerHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(10240)
        decoded_data = bytes.decode(data)
        if decoded_data == "init":
            self.request.send(decoded_data.encode('utf-8'))
        elif decoded_data == "live":
            data = get_last_packet('13')
            self.request.send(pickle.dumps(data))
        return


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True

    def __init__(self, server_address, handler_class=ServerHandler):
        socketserver.ThreadingTCPServer.__init__(self, server_address, handler_class)
        return

    @threaded
    def serve_forever(self, poll_interval=0.5):
        while True:
            self.handle_request()
        return