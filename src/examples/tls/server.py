import ssl
import socket

# Create a standard socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(("localhost", 8443))
server_socket.listen(5)

# Wrap with SSL
server_cert = 'keys/server.crt'
server_key = 'keys/server.key'
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile=server_cert, keyfile=server_key)

with context.wrap_socket(server_socket, server_side=True) as ssl_socket:
    print("Server listening on port 8443...")
    conn, addr = ssl_socket.accept()
    print(f"Connected by {addr}")
    data = conn.recv(1024)
    conn.sendall(b"Hello, SSL!")
    conn.read()
    conn.close()

# --
server_socket.close()

