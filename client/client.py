import socket
import sys

HOST, PORT = "10.211.55.4", 65535
data = " ".join(sys.argv[1:])

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    encoded_data = data.encode('utf8')
    sock.sendall(encoded_data)

    # Receive data from the server and shut down
    received = sock.recv(1024)
finally:
    sock.close()

decoded_data = bytes.decode(received)

print("Sent:     {}".format(data))
print("Received: {}".format(decoded_data))