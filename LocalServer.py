import socket
import threading
from random import shuffle
import time

PORT = 5050
#SERVER = socket.gethostbyname(socket.gethostname())
HOST = socket.gethostbyname(socket.gethostname())
ADDR = (HOST, PORT)
#When we bind our socket to a specific address, 
# the address needs to be in a tuple. (HOST,PORT)
HEADER = 16
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

#AF_INET - over the internet
#socket.SOCK_STREAM - streaming data throught the socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
#To bind the socket to this address
#anything that connects to the socket connects to this address


class Player:
    '''class used in creating player objects for clients'''

    playerCount = 0
    playerList = []
    usernameList = []

    def __init__(self,username,client,address):
        '''constructor of the class'''
        self.username = username
        self.score = 0
        self.client = client
        self.address = address

        while self.username in Player.usernameList:
            self.username = self.username + "_"
        
        Player.playerCount += 1
        Player.playerList.append(self)
        Player.usernameList.append(self.username)

    def deletePlayer(self):
        '''deletes the player object'''
        Player.playerCount -= 1
        Player.playerList.remove(self)
    


def useQuestions():
    '''function used in getting questions from questions.txt'''
    with open("questions.txt", "r") as file:
        
        singleLine = file.readline()
        dict = eval(singleLine)

    return dict

def broadcast(message):
    '''function used in broadcasting messages to all clients'''
    for player in Player.playerList:
        player.client.send(message.encode(FORMAT))

def main():
    '''main function that deals with client requests'''

    server.listen()
    #listens for new connections
    while True:
        clientObject, address = server.accept()
        #accepts new connections
        clientObject.send("!USERNAME".encode(FORMAT))
        #asks for username
        username = clientObject.recv(512).decode(FORMAT)
        player = Player(username,clientObject,address)
        #player object is created
        clientThread = threading.Thread(target=handle_client,\
            args=(clientObject,player))
        #a client thread starts running handling 
        # all messages with the client
        clientThread.start()
        
        print(f"\n[ACTIVE CONNECTIONS] \
{threading.activeCount()-3}")

def handle_client(clientObject,player):
    '''handles all messages regarding one client'''

    global items
    global options
    global n

    userName = player.username
    print(f"[NEW CONNECTION] {userName} connected.")
    connected = True

    while connected:

        msg = clientObject.recv(512).decode(FORMAT)

        if msg: # if msg is not static

            if msg.startswith("!Start Game"):
                #client asks server to start game

                if Player.playerCount>1:
                    #if there is two players, game starts

                    gameThread = threading.Thread(target=game)
                    time.sleep(1)
                    gameThread.start()
                    statement = "Multiplayer has started|"

                else:
                    statement = "Waiting for players|"
                    #server tells the client to wait
                
            elif msg.startswith("!Update score"):
                #to update the score in the player object
                #  and to broadcast it

                player.score = int(msg.split(":")[1])
                tuple = ()

                for pl in Player.playerList:
                    
                    tuple += ((pl.username,pl.score),)

                else:

                    broadcast(f"Current Score|{str(tuple)}|")

            if msg == DISCONNECT_MESSAGE:
                #client has disconnected

                connected = False
                print(f"[DISCONNECTION] \
{userName} has disconnected.")
                player.deletePlayer()

                if len(Player.playerList) == 0:
                    #if all players have disconnected

                    print("[SERVER SHUT DOWN] \
All players have disconnected.")
                    exit()
            else:

                broadcast(statement)

    clientObject.close()

#initial question variables
n = 0
dict_qs = useQuestions()
items = list(dict_qs.items())
shuffle(items)
correctAns = items[n][1][3]
options = items[n][1][0:4]
shuffle(options)

def game():
    '''game thread that broadcasts all
    the questions'''
    global n
    global items

    while True:

        n+=1

        try:

            correctAns = items[n][1][3]

        except IndexError:

            print("[GAME OVER] Game has ended")
            broadcast("End Game")
            break

        options = items[n][1][0:4]
        shuffle(options)
        statement = f"Question|{str(items[n][0])}\
|{options}|{correctAns}|"
        broadcast(statement)
        time.sleep(11)

serverThread = threading.Thread(target=main)
serverThread.start()
#server thread starts running

print("[STARTING] server is starting...")