# openssl req -x509 -newkey rsa:4096 -keyout server.key -out server.crt -days 365 -nodes
import ssl
import socket

context = ssl.create_default_context()
context.load_verify_locations("/path/to/ca.crt")  # Optional: custom CA

with socket.create_connection(("localhost", 8443)) as sock:
    with context.wrap_socket(sock, server_hostname="localhost") as ssl_sock:
        print(f"SSL version: {ssl_sock.version()}")
        ssl_sock.sendall(b"Hello, server!")
        data = ssl_sock.recv(1024)
        print(f"Received: {data}")
        
# ------------------------
import ssl
import socket
# Create a standard socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("localhost", 8443))
server_socket.listen(5)

# Wrap with SSL
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="server.crt", keyfile="server.key")

with context.wrap_socket(server_socket, server_side=True) as ssl_socket:
    print("Server listening on port 8443...")
    conn, addr = ssl_socket.accept()
    print(f"Connected by {addr}")
    data = conn.recv(1024)
    conn.sendall(b"Hello, SSL!")