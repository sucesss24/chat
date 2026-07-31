import socket

HOST = '127.0.0.1'
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print("Server is waiting for connection...")

conn, addr = server.accept()
print("Connected by:", addr)

while True:
    client_msg = conn.recv(1024).decode()

    if not client_msg:
        break

    print("Client:", client_msg)

    if client_msg.lower() == "bye":
        break

    server_msg = input("Server: ")
    conn.send(server_msg.encode())

    if server_msg.lower() == "bye":
        break

conn.close()
server.close()