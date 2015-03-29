import socketserver
import threading


def threaded(fn):
    def wrapper(*args, **kwargs):
        threading.Thread(target=fn, args=args, kwargs=kwargs).start()
    return wrapper


class ServerHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024)
        self.request.send(data)
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