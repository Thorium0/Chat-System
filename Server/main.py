import socket, select, sys
from threading import Thread

IP_address = "0.0.0.0"
Port = 2478

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((IP_address, Port))
server.listen(100)
list_of_clients = []

def clientthread(conn, addr):
    conn.send(b"Welcome to this chatroom!\n")
    while True:
            try:
                message = conn.recv(2048).decode('utf-8')
                if message:
                    message = message.split(";")
                    message_to_send = "[" + message[0] + "]: " + message[1] +"\n"
                    print ("<" + addr[0] + ">" + message_to_send)
                    broadcast(message_to_send, conn)
                else:
                    remove(conn)

            except:
                continue

def broadcast(message, connection):
    for client in list_of_clients:
        if client != connection:
            try:
                client.send(message.encode('utf-8'))
            except:
                client.close()
                remove(client)


def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

if __name__ == '__main__':
    print("Ready for connections...")
    while True:
        conn, addr = server.accept()
        list_of_clients.append(conn)
        print (addr[0] + " connected")
        Thread(target=clientthread, args=(conn,addr)).start()

conn.close()
server.close()
