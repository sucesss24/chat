import socket

HOST = '127.0.0.1'
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

while True:
    msg = input("Client: ")
    client.send(msg.encode())

    if msg.lower() == "bye":
        break

    server_reply = client.recv(1024).decode()
    print("Server:", server_reply)

    if server_reply.lower() == "bye":
        break

client.close()