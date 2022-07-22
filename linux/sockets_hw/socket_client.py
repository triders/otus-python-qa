import socket
import sys

HOST = "127.0.0.1"
PORT = None

try:
    PORT = int(sys.argv[1])
except IndexError:
    print("Please, type the server port number to connect!")
    exit(1)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_client:
    print(f"\nConnecting to server: {HOST}:{PORT}...")
    socket_client.connect((HOST, PORT))
    print("Successfully established a connection!",
          "To exit type 'close', 'exit' or 'meow'", "",
          r"Type a request to server in the HTTP format, e.g.:",
          r"    GET / HTTP/1.1\r\nHeader 1: one\r\nHeader 2: two\r\nContent-Type: text/html\r\n\r\n",
          "OR",
          r"Type 'path:path/to/file' to send a HTTP request from a text file", "", sep="\n")
    while True:

        data_to_send = input("(HTTP REQUEST) >>> ")

        if data_to_send in ('close', 'exit', 'meow'):
            socket_client.send(data_to_send.encode("utf-8"))
            print("Closing the connection...")
            break
        elif data_to_send.startswith('path'):
            file_path = data_to_send.split("path:")[1]
            with open(file_path, 'r') as file:
                data_to_send = file.read()

        socket_client.send(data_to_send.encode("utf-8"))

        # socket_client.send(bytes(data_to_send.strip(), "utf-8"))
        data = socket_client.recv(1024)

        print('(SERVER RESPONDED) >>> ', repr(data.decode("utf-8")))
