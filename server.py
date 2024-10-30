# socket library - low-level networking interface, networking functionality
# threading library - allows eahc client to run on its own thread for
# simultaneous communication
import socket
import threading

# Server setup
host = '10.94.102.3'  # Localhost (for testing locally)
port = 12345        # Port to listen on

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creates TCP socket for the server
server.bind((host, port)) # binds socket to address and port
server.listen() # listens for incoming clients

# stores client sockets and nicknames
clients = []
nicknames = []

# Broadcast message to all connected clients
def broadcast(message):
    for client in clients:
        client.send(message)

# Handle individual client connection
# receives and broadcasts messafes from a specific client
def handle_client(client):
    while True:
        try:
            # Receiving message from client
            message = client.recv(1024)
            broadcast(message)
        except: # if an error occurs
            # Remove and close clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat.'.encode('utf-8'))
            nicknames.remove(nickname)
            break

# Accepting new clients
def receive():
    while True: #accepts incoming connections and starts a thread for each
        client, address = server.accept() # waits for and accepts new client
        print(f"Connected with {str(address)}")

        # Request and store nickname
        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of the client is {nickname}!')
        broadcast(f'{nickname} joined the chat!'.encode('utf-8'))
        client.send('Connected to the server!'.encode('utf-8'))

        # Start handling the client in a new thread
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

print("Server is listening...")
receive()
