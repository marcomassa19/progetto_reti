from socket import AF_INET, socket, SOCK_STREAM, error as SocketError
from threading import Thread

def accept_incoming_connections():
    while True:
        try:
            client, client_address = SERVER.accept()
            print("%s:%s connected." % client_address)
            client.send(bytes("Greetings! Enter your Name followed by Enter key!", "utf8"))
            addresses[client] = client_address
            Thread(target=handle_client, args=(client,)).start()
        except SocketError as e:
            print("An error occurred while accepting connections:", e)
            break

def handle_client(client):  
    try:
        name = client.recv(BUFSIZ).decode("utf8")
        welcome = 'Welcome %s! If you want to leave the Chat, type {quit} to exit.' % name
        client.send(bytes(welcome, "utf8"))
        msg = "%s joined the chat!" % name
        broadcast(bytes(msg, "utf8"))
        clients[client] = name
        
        while True:
            msg = client.recv(BUFSIZ)
            if msg != bytes("{quit}", "utf8"):
                broadcast(msg, name+": ")
            else:
                client.send(bytes("{quit}", "utf8"))
                client.close()
                del clients[client]
                broadcast(bytes("%s left the Chat." % name, "utf8"))
                break
    except SocketError as e:
        print("An error occurred while handling client:", e)

def broadcast(msg, prefix=""):
    for user in clients:
        try:
            user.send(bytes(prefix, "utf8")+msg)
        except SocketError as e:
            print("An error occurred while broadcasting message to user:", e)

clients = {}
addresses = {}

HOST = ''
PORT = 1918
BUFSIZ = 1024
ADDR = (HOST, PORT)

try:
    SERVER = socket(AF_INET, SOCK_STREAM)
    SERVER.bind(ADDR)

    SERVER.listen(5)
    print("Waiting for connections...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()

except SocketError as e:
    print("An error occurred:", e)
