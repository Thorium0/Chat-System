import socket, select, sys, ipaddress, netifaces
from threading import Thread

IP_address = "0.0.0.0"
Port = 2478

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((IP_address, Port))
server.listen(100)
list_of_clients = []
admins = []

def clientthread(conn, addr):
    conn.send(b"\nWelcome to this chatroom!\n")
    while True:
            try:
                message = conn.recv(2048).decode('utf-8')
                if message:
                    message = message.split("¬")
                    if message[1][0] == "/":
                        if conn.getpeername()[0] in admins:
                            result = executeUserCommand(message)
                            if result == "die":
                                return
                            continue
                        else:
                            message_to_send = "\n<You are not allowed to use commands>"
                            conn.send(message_to_send.encode("utf-8"))
                            continue

                    message_to_send = "[" + message[0] + "]: " + message[1] +"\n"
                    print ("\n<" + addr[0] + ">" + message_to_send)
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


def executeUserCommand(message):
    user = message[0]
    command = message[1][1:].split()
    if command[0] == "kick":
        try:
                for client in list_of_clients:
                    if client.getpeername()[0] == command[1]:
                        print("\n" + user + " has been kicked")
                        client.send("\n<You have been kicked by an admin>".encode("utf-8"))
                        broadcast("\n<" + user + " has been kicked an admin>", client)
                        remove(client)
                        client.close()
                        return "die"

        except:
            pass


def awaitCommands():
    while True:
        rawInput = input("\n>>> ")
        command = rawInput.split()

        try:
            if command[0] == "admin":
                options = "Available options are: [grant, revoke, list]"
                try:
                    if command[1] == "grant":
                        admins.append(command[2])
                    elif command[1] == "revoke":
                        try: admins.remove(command[2])
                        except: print("Ip not in admin list")
                    elif command[1] == "list":
                        print(admins)
                    else:
                        print(options)
                except:
                    print(options)

            elif command[0] == "client":
                options = "Available options are: [list]"
                try:
                    if command[1] == "list":
                        print(list_of_clients)
                    else:
                        print(options)
                except:
                    print(options)

            else:
                print("Unrecognized command")
        except:
            if command:
                print("Invalid input")






if __name__ == '__main__':
    local_ip = netifaces.ifaddresses("wlo1")[2][0]["addr"]
    print("Running on {}".format(local_ip))
    print("Ready for connections...")
    Thread(target=awaitCommands).start()
    while True:
        conn, addr = server.accept()
        list_of_clients.append(conn)
        print ("\n" + addr[0] + " connected")
        Thread(target=clientthread, args=(conn,addr)).start()


conn.close()
server.close()
