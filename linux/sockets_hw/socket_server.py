import sys
import datetime
import socket
import random
from http import HTTPStatus

LOCALHOST = "127.0.0.1"


def random_port():
    return random.randint(20000, 30000)


with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) as server_socket:
    address_and_port = (LOCALHOST, random_port())
    server_socket.bind(address_and_port)
    try:
        backlog = int(sys.argv[1])
    except IndexError:
        print("No 'backlog' argument specified. Using 10 - default backlog connections size")
        backlog = 10

    server_socket.listen(10)

    print('', f'Hi! This is a simple HTTP server: {address_and_port[0]}:{address_and_port[1]}',
          "Send me an HTTP requests and I will response", sep="\n")

    while True:

        conn, addr = server_socket.accept()

        with conn:

            print('', f'Client {addr} just connected!\n', sep=f"\n{'*' * 50}\n")

            while True:

                try:
                    data_in_bytes = conn.recv(1024)
                    # example: b'GET / HTTP/1.1\r\Header 1: one\r\nHeader 2: two\r\nContent-Type: text/html\r\n\r\n'

                    if data_in_bytes in (b'close', b'exit', b'meow'):
                        print(
                            f'Got termination signal: {data_in_bytes} from {addr}, and closed connection.\nFarewell!\n')
                        conn.close()
                        break

                    data = data_in_bytes.decode('utf-8')
                    print("", f"Received data: '{data}'\nfrom: {addr}\n", sep=f"\n{'>' * 50}\n")

                    try:
                        data_in_list = data.split("\r\n")
                        request_line = data_in_list[0]
                        request_method = data_in_list[0].split(" ")[0]
                        request_headers = data_in_list[1:-2]
                    except:
                        conn.send(b'Invalid HTTP request. Please, double-check it o_0')
                        continue

                    try:
                        request_status = int(request_line.split('status=')[1].split(' HTTP')[0])
                        status = HTTPStatus(request_status)
                    except:
                        status = HTTPStatus(200)

                    body = (
                        f'<h1>Hello, stranger!</h1>'
                        f'<h3>{datetime.datetime.now()}</h3>'
                        f'<div></div>'
                        f'<h3>Stats about your request:</h3>'
                        f'<div>Request Method: {request_method}</div>'
                        f'<div>Request Source: {address_and_port}</div>'
                        f'<div>Response Status: {status.value} {status.name}</div>'
                        f'<div></div>'
                        f'<img src="https://i.kym-cdn.com/entries/icons/original/000/006/877/707538ef3afa883c1d146b42cf01bac2.jpg">'
                    )

                    # also, let's show all original request headers in the HTML body
                    for header in request_headers:
                        body += f'<div>{header}</div>'

                    response_line = f'HTTP/1.1 {status.value} {status.name}'
                    headers = '\r\n'.join([
                        response_line,
                        f'Content-Length: {len(body)}',
                        'Content-Type: text/html',
                        *request_headers
                    ])

                    response = '\r\n\r\n'.join([
                        headers,
                        body
                    ])
                    print(f"Responded to {addr} with data: \n'{response}'", "", f"\n{'<' * 50}\n")

                    conn.send(response.encode('utf-8'))
                except:
                    conn.close()
