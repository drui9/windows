import ssl
import socket

server_cert = 'keys/server.crt'
context = ssl.create_default_context()
context.load_verify_locations(server_cert)

with socket.create_connection(("localhost", 8443)) as sock:
    with context.wrap_socket(sock, server_hostname="localhost") as ssl_sock:
        print(f"SSL version: {ssl_sock.version()}")
        ssl_sock.sendall(b"Hello, server!")
        data = ssl_sock.recv(1024)
        print(f"Received: {data}")
        ssl_sock.sendall(b'close')


