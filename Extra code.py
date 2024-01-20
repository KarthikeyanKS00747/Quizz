import socket
import threading
from random import shuffle
import time

PORT = 5050
#SERVER = socket.gethostbyname(socket.gethostname())
HOST = "192.168.100.8"
ADDR = (HOST, PORT)
#When we bind our socket to a specific address, the address needs to be in a tuple. (HOST,PORT)
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
    playerCount = 0
    playerList = []
    

    def __init__(self,username,client,address):
        self.username = username
        self.score = 0
        self.client = client
        self.address = address
        Player.playerCount += 1
        Player.playerList.append(self.username)

    def correctAns(self):
        self.score += 1

    def returnScore(self):
        return self.score

    def clientObject(self):
        return self.client

    def userName(self):
        return self.username

    def deletePlayer(self):
        Player.playerCount -= 1
        Player.playerList.remove(self.userName())

def useQuestions():

    with open("questions.txt", "r") as file:
        
        singleLine = file.readline()
        dict = eval(singleLine)

    return dict

def broadcast(message):
    for player in Player.playerList:
        player.clientObject.send(message)

def main():
    server.listen()
    while True:
        clientObject, address = server.accept()
        clientObject.send("!USERNAME".encode(FORMAT))
        username = clientObject.recv(512).decode(FORMAT)
        player = Player(username,clientObject,address)
        clientThread = threading.Thread(target=handle_client,args=(clientObject,player))
        clientThread.start()
        
        print(f"\n[ACTIVE CONNECTIONS] {threading.activeCount()-2}")
        

def handle_client(clientObject,player):
    userName = player.userName()
    print(f"[NEW CONNECTION] {userName} connected.")
    connected = True

    while connected:
        msg = clientObject.recv(512).decode(FORMAT)
        if msg:
            print(f"{userName}|{msg}")
            message = handle_message(msg)
            print(message)
            if msg == DISCONNECT_MESSAGE:
                connected = False
                print(f"[DISCONNECTION] {userName} has disconnected.")
                player.deletePlayer()
            else:
                clientObject.send(message.encode(FORMAT))

    clientObject.close()

n = 0
dict_qs = useQuestions()
items = list(dict_qs.items())
shuffle(items)
correctAns = items[n][1][3]
options = items[n][1][0:4]
shuffle(options)


def handle_message(msg):
    global items
    global options
    global n
    
    if msg.startswith("!Next Question"):
        n += 1
        try:
            correctAns = items[n][1][3]
        except IndexError:
            n=0
            correctAns = items[n][1][3]
        options = items[n][1][0:4]
        shuffle(options)
        statement = f"Next Question|{str(items[n][0])}|{options}|{correctAns}"
        return statement

    elif msg.startswith("!Previous Question"):
        n -= 1
        correctAns = items[n][1][3]
        options = items[n][1][0:4]
        shuffle(options)
        statement = f"Previous Question|{str(items[n][0])}|{options}|{correctAns}"
        return statement

serverThread = threading.Thread(target=main)
serverThread.start()

print("[STARTING] server is starting...")

'''def handle_client(conn,addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True

    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
            print(f"[{addr} {msg}]")
            
            
            conn.broadcast(handle_message("!Next Question").encode())
    conn.close()

    
def start():
    server.listen()
    #server listens for new connections
    while True:
        conn, addr = server.accept()
        #waits for a new connection
        #stores the address (ip address and port it came from) of any new connection
        #stores a socket object that allows us to send and recieve messages
        clientThread = threading.Thread(target=handle_client,args=(conn,addr))

        clientThread.start()
        print(f"\n[ACTIVE CONNECTIONS] {threading.activeCount()-2}")
        
            
        #no. of active connections

n = 0
dict_qs = useQuestions()
items = list(dict_qs.items())
shuffle(items)
correctAns = items[n][1][3]
options = items[n][1][0:4]
shuffle(options)

serverThread = threading.Thread(target=start)
serverThread.start()

print("[STARTING] server is starting...")'''

print("--------------------------------------------")
import socket
import threading
import time

from tkinter import messagebox
import tkinter as tk


window = tk.Tk()
window.geometry("550x600")
window.title("Quizz")
window.configure(bg='#001F3F')

#STATIC VARIABLES
PORT = 5050
CLIENT = "192.168.100.8"
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
ADDR = (CLIENT,PORT)

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(ADDR)
n = 0
dict={}
score = 0

def send(msg):
    message = msg.encode(FORMAT)
    client.send(message)

def clientInterface():
    global n
    global question
    global correctAns
    global options
    
    while True:
        message = client.recv(1024).decode(FORMAT)
        print(message)
        list1 = message.split("|")
        question = list1[1].rstrip("|")
        print("1",question,type(question))
        options = eval(list1[2].rstrip("|"))
        print("2",options,type(options))
        correctAns = list1[3].rstrip("|")
        print("3",correctAns,type(correctAns))

def handle_queries(message):
    if message.startswith(("!USERNAME",)):
        send('batman')
        recieveThread = threading.Thread(target=clientInterface)
        recieveThread.start()
        send("!Next Question")
        time.sleep(1)

message = client.recv(512).decode(FORMAT)
handle_queries(message)

def eventListener(event,ans=None):
    global n
    global question
    global correctAns
    global options
    global score

    for buttonOption in (0,1,2,3):
        changeColour(buttonOption,"#39CCCC")

    if event == "Next Question":

        n += 1

        send("!Next Question")
        time.sleep(1)
        statement = f"{n+1}. {question}"
        
        questionLabel.config(text=statement)
        ansOptionA.config(text=f"a) {returnOption(0)}")
        ansOptionB.config(text=f"b) {returnOption(1)}") 
        ansOptionC.config(text=f"c) {returnOption(2)}") 
        ansOptionD.config(text=f"d) {returnOption(3)}")
        revealLabel.config(text="")
        
    elif event == "Previous Question":

        n -= 1

        send("!Previous Question")
        time.sleep(1)
        statement = f"{n+1}. {question}"
        questionLabel.config(text=statement)
        ansOptionA.config(text=f"a) {returnOption(0)}")
        ansOptionB.config(text=f"b) {returnOption(1)}") 
        ansOptionC.config(text=f"c) {returnOption(2)}") 
        ansOptionD.config(text=f"d) {returnOption(3)}")
        revealLabel.config(text="")

    elif event == "Check Answer":
        for buttonOption in (0,1,2,3):
                if dict[buttonOption] == "correct answer":
                    changeColour(buttonOption,"#2ECC40")
                else:
                    changeColour(buttonOption,"#FF851B")

        if ans == correctAns:
            revealLabel.config(text="Correct Answer!!!")
            score += 1
        else:
            revealLabel.config(text="Incorrect Answer")
            score -= 1
            
def changeColour(buttonOption,colour):
    if buttonOption == 0:
        ansOptionA.config(fg=colour)
    elif buttonOption == 1:
        ansOptionB.config(fg=colour)
    if buttonOption == 2:
        ansOptionC.config(fg=colour)
    if buttonOption == 3:
        ansOptionD.config(fg=colour)

def returnOption(option):
    global n
    global items
    global options
    global dict
    global correctAns

    if options[option] == correctAns:
        dict[option] = "correct answer"
    else:
        dict[option] = "incorrect answer"

    return options[option]

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        window.destroy()
        send("!DISCONNECT")  

window.protocol("WM_DELETE_WINDOW", on_closing)

statement = f"{n+1}. {question}"
questionLabel = tk.Label(window,text=statement,font=('Helvetica',16),bg='#001F3F',fg="#39CCCC",wraplength=480)
nextQuestion = tk.Button(window, text="Next Question", command=lambda : eventListener("Next Question"),bg='#001F3F',fg="#39CCCC",padx=20)
prevQuestion = tk.Button(window, text="Previous Question", command=lambda : eventListener("Previous Question"),bg='#001F3F',fg="#39CCCC",padx=20)
ansOptionA = tk.Button(window, text=f"a) {returnOption(0)}", command=lambda : eventListener("Check Answer",returnOption(0)),padx=20,font=('Helvetica',14),bg='#001F3F',fg="#39CCCC",wraplength=480) 
ansOptionB = tk.Button(window, text=f"b) {returnOption(1)}", command=lambda : eventListener("Check Answer",returnOption(1)),padx=20,font=('Helvetica',14),bg='#001F3F',fg="#39CCCC",wraplength=480) 
ansOptionC = tk.Button(window, text=f"c) {returnOption(2)}", command=lambda : eventListener("Check Answer",returnOption(2)),padx=20,font=('Helvetica',14),bg='#001F3F',fg="#39CCCC",wraplength=480) 
ansOptionD = tk.Button(window, text=f"d) {returnOption(3)}", command=lambda : eventListener("Check Answer",returnOption(3)),padx=20,font=('Helvetica',14),bg='#001F3F',fg="#39CCCC",wraplength=480) 
revealLabel = tk.Label(window,bg='#001F3F',fg="#39CCCC")
questionLabel.pack(pady=20)
nextQuestion.pack(pady=10)
prevQuestion.pack(pady=10)
#optionA.pack(pady=10)
ansOptionA.pack(pady=10)
#optionB.pack(pady=10)
ansOptionB.pack(pady=10)
#optionC.pack(pady=10)
ansOptionC.pack(pady=10)
#optionD.pack(pady=10)
ansOptionD.pack(pady=10)
revealLabel.pack(pady=5)
window.mainloop()

'''
root = tk.Tk()

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()'''

print("----------------------------")
'''
def singlePlayer(username,guest=False):

    import json
    global optionsCharList

    dict_qs = useQuestions()

    imp = {}
    qno = 0
    print("_"*48)
    print()

    while True:

        for question,optionsList in dict_qs.items():                 #key-question;answerList-options in the form of a list

            optionsList = optionsList[0:4]
            qno += 1                                                 #num_1-numbering of questions
            print(str(qno)+".", question, sep = "")                  #printing the numbering and the question
            correct_ans = optionsList[3]                             #defining the variable correct_ans to store 4th element of the options in a list
            random.shuffle(optionsList)                              #shufflling of options

            for optionChar,option in zip(optionsCharList,optionsList): 

                print(optionChar, option)                            #printing of options with alphabetical numbering

            while True:                                              #answer checking segment

                ans = input("Enter the option: ")                    #answer from the user
                print()

                if ans == "skip":                                    #to skip a question

                    break

                if ans.startswith(optionsCharList):                  #to find if the answer exists as an element in the list of options

                    ans = ans.lstrip("a.")
                    ans = ans.lstrip("b.")
                    ans = ans.lstrip("c.")
                    ans = ans.lstrip("d.")

                elif ans == "imp":                                   #to mark an important question

                    print("The marked questions are: ")
                    print(json.dumps(imp, indent=2))                 #to pretty print a dictionary
                    print()
                    ans = "skip"                                     #skips a while loop at the end
                    break

                if ans == correct_ans:                               #Checking of correct answer

                    print("Correct answer!!!")
                    print()
                    break

                else:

                    for option in optionsList:                       #Checking if its an incorrect answer

                        if ans == option:

                            print("Incorrect answer")
                            print()
                            print(correct_ans, "is the correct answer.")
                            print()
                            break

                        else:

                            pass

                    else:

                        print("Incomplete answer")                   #Checking if it's an incomplete answer
                        print()
                        continue

                    break

            while ans != "skip":                                     #while loop for marking a question as a important one

                print("Was the question hard, complicated or important enough?")
                ans=input("Type 'yes' or 'no': ")
                print()

                if ans == "yes":

                    imp[question] = optionsList                      #important question and answer is being defined
                    break

                elif ans == "no":

                    break

                else:

                    print("Response is not defined.\nTry Again")

            else:

                continue
menu()
'''
"""
if event == "Next Question":

        n += 1

        send("!Next Question")
        statement = f"{n+1}. {question}"
        questionLabel.config(text=statement)
        ansOptionA.config(text=f"a) {returnOption(0)}")
        ansOptionB.config(text=f"b) {returnOption(1)}") 
        ansOptionC.config(text=f"c) {returnOption(2)}") 
        ansOptionD.config(text=f"d) {returnOption(3)}")
        scoreLabel.config(text="")
        
    elif event == "Previous Question":

        n -= 1

        send("!Previous Question")
        time.sleep(1)
        statement = f"{n+1}. {question}"
        questionLabel.config(text=statement)
        ansOptionA.config(text=f"a) {returnOption(0)}")
        ansOptionB.config(text=f"b) {returnOption(1)}") 
        ansOptionC.config(text=f"c) {returnOption(2)}") 
        ansOptionD.config(text=f"d) {returnOption(3)}")
        scoreLabel.config(text="")"""

'''def handle_client(conn,addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True

    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
            print(f"[{addr} {msg}]")
            
            
            conn.broadcast(handle_message("!Next Question").encode())
    conn.close()

    
def start():
    server.listen()
    #server listens for new connections
    while True:
        conn, addr = server.accept()
        #waits for a new connection
        #stores the address (ip address and port it came from) of any new connection
        #stores a socket object that allows us to send and recieve messages
        clientThread = threading.Thread(target=handle_client,args=(conn,addr))

        clientThread.start()
        print(f"\n[ACTIVE CONNECTIONS] {threading.activeCount()-2}")
        
            
        #no. of active connections

n = 0
dict_qs = useQuestions()
items = list(dict_qs.items())
shuffle(items)
correctAns = items[n][1][3]
options = items[n][1][0:4]
shuffle(options)

serverThread = threading.Thread(target=start)
serverThread.start()

print("[STARTING] server is starting...")'''

def deleteQuestions(username):

    with open("questions.txt", "r+") as file:
        
        singleLine = file.readline()
        dict = eval(singleLine)
        print(type(dict))
        print()

        while True:

            question = input("Enter the Question : ")
            print()

            if question in dict:

                print("Question Found.")

                if (username == dict[question][4][0]) or (username == "Admin"):
                    del dict[question]
                    singleLine = str(dict)
                    file.seek(0)
                    file.write(singleLine)
                    print()
                    print("Question has been deleted successfully.")
                    print()
                    break

                else:
                    print("You do not have the permission to delete this question.")
                    print()
                    
            else:

                print("Question does not exist")
'''      
 if msg.startswith("!Next Question"):
                #client asks for a new question
                n += 1
                try:
                    correctAns = items[n][1][3]
                    options = items[n][1][0:4]
                    shuffle(options)
                    statement = f"Next Question|{str(items[n][0])}|{options}|{correctAns}"
                except:
                    pass

            elif msg.startswith("!Previous Question"):

                n -= 1
                correctAns = items[n][1][3]
                options = items[n][1][0:4]
                shuffle(options)
                statement = f"Previous Question|{str(items[n][0])}|{options}|{correctAns}"'''