import mysql.connector #for connecting to the database
import socket #for  connecting to a server
import threading #for creating threads within the file
# such as the server etc
import time #for importing time.sleep
from tkinter import messagebox 
#to create a messagebox when the tkinter window is prompted to close
import tkinter as tk #tkinter deals with the GUI of the program

def addQuestions(username):
    '''Used to add questions to questions.txt'''

    with open("questions.txt", "r+") as file: 
        #opens questions.txt with read and write mode
        
        singleLine = file.readline() 
        #the file contains all the questions as a 
        #string of a dictionary in one line
        dict = eval(singleLine) 
        #the string of dictionary is evaluated into a dictionary
        print()

        while True:

            question = input("Enter the Question \
to be added : ") 
            #prompts the user to type in the question to be added

            if question == "done":
                break
            elif question in dict: #In the scenario that the given 
                #question already exists

                print("Question already in directory.")
                print("Please try again.")
                continue
            
            print("Please enter the fourth \
option as the correct answer.") 
            #the dict is defined in such a way that 3
            #the fourth option is the correct answer

            print()

            options = [input(f"Enter option {x} : ")\
                for x in range(1,5)]
            #text puntuation for getting 
            # four input values as options
            dict[question] = options + [(username,)]
            #format of every question in the dictionary
            #overwrites the old singleline for the new one

        file.seek(0)
        file.write(str(dict))
        print()
        print("Question has been saved successfully.")
        print()
        

def deleteUser(username):
    '''Function used to delete users which is only 
    accessible to the admin'''

    if username != "Admin": #checks if username is "Admin"

        print("Please login as Admin to delete users.")
        return None

    connection = mysql.connector.connect(host='localhost',\
user='root', passwd='CsMath@007', database='Quiz',\
    auth_plugin='mysql_native_password')
    #connects to the mysql database Quiz
    sqlCursor = connection.cursor()
    #creates a new cursor object
    sqlCursor.execute("""SELECT Username FROM LoginData;""")

    list = sqlCursor.fetchall() 
    #fetches Username and Password as a tuple
    usernames = [tuple[0] for tuple in list]
    #text puntuation for producing all usernames into a list
    username = input("Enter the username to be deleted : ")

    while username not in usernames:#if username does not exist

        print()
        print("Username does not exist in the database.")
        print("Please try again.")
        print()
        username = input("Enter the username : ")
        #to enter the username again

    else:

        print()
        sqlCursor.execute(\
f"""DELETE FROM LoginData WHERE Username="{username}";""")
#deletes the record of the given username
        print(f"The login credentials of {username} \
have been successfully deleted.")
        connection.commit()
        #saves the changes
        connection.close()

def createAccount():
    '''Function used to create an account'''

    connection = mysql.connector.connect(host='localhost',\
user='root', passwd='CsMath@007', database='Quiz',\
auth_plugin='mysql_native_password')
    #connects to the mysql database
    sqlCursor = connection.cursor()
    #creates a new cursor object

    commands = ("""CREATE DATABASE Quiz;""","""USE Quiz;"""\
,"""CREATE TABLE LoginData(ID INTEGER PRIMARY KEY, \
Username VARCHAR(50), Password VARCHAR(255));""",\
"""SELECT Username,Password FROM LoginData;""",\
"""ALTER TABLE LoginData AUTO_INCREMENT=100;""")
    sqlCursor.execute(commands[3])
    list = sqlCursor.fetchall()
    #returns list of tuples containg username and password

    while True:

        username = input("Enter the username : ")

        for tuple in list:

            if tuple[0] == username:
                #if username already exists

                print("Username is already taken")
                print("Try another one.")
                break
        else:

            while True:  

                print()
                password = input("Enter the password : ")

                if len(password) < 8:
                    #if password contains less than
                    # 8 characters
                    print(\
"Password should contain atleast 8 characters.")
                    print("Please try again.")

                else:

                    command = \
f"""INSERT into LoginData(Username,Password) \
VALUES("{username}","{password}");"""
                    sqlCursor.execute(command)
                    connection.commit()
                    #changes are saved
                    connection.close()

                    print()
                    print(\
"You have successfully created an account.")

                    return

def loginAccount():
    '''Function used to login to an account'''

    connection = mysql.connector.connect(\
host='localhost', user='root', \
passwd='CsMath@007', database='Quiz',\
auth_plugin='mysql_native_password')
    #connects to the mysql database quiz
    sqlCursor = connection.cursor()
    #creates a new cursor object
    commands = (\
"""CREATE DATABASE Quiz;""","""USE Quiz;""",
"""CREATE TABLE LoginData(ID INTEGER PRIMARY KEY,\
 Username VARCHAR(50), Password VARCHAR(255));""",\
"""SELECT Username,Password FROM LoginData;""",\
"""ALTER TABLE LoginData AUTO_INCREMENT=100;""")
    sqlCursor.execute(commands[3])
    list = sqlCursor.fetchall()
    #returns list of tuples containg username and password

    while True:
            
        print()
        username = input("Enter the username : ")

        for tuple in list:

            if tuple[0] == username:
                #Username is found

                print("Username found.")

                while True:

                    print()
                    password = input("Enter the password : ")

                    if password == tuple[1]:
                        #password is correct

                        print("You have successfully logged in.")
                        print()
                        print("Welcome back,", username)
                        
                        return username

                    else:

                        print("Password is incorrect.")
                        print("Please try again.")

        else:
            
            print("Username does not exist in the database.")
            print("Please try again")

def startServer():
    '''target function in the main file used to start
    a server thread'''
    import LocalServer #imports the file


def menu():
    '''main interface of the program'''

    print('''
                                                            ||MENU||

1. Login to an existing Quizz profile.
2. Create a new Quizz profile.
    ''')

    response = input("Enter the option : ")
    print()

    if response.startswith("1"):

        username = loginAccount()
        print("_"*48)
        print('''
        What would you like to do?

1. Singleplayer Start Game
2. Multiplayer Start Game
3. Multiplayer Join Game
4. Add Questions
5. Delete Users [ADMIN ACCESS REQUIRED]
        ''')

        response = input("Enter the option : ")
        print()

        if response.startswith("1"):

            import Singleplayer #imports the file
        
        elif response.startswith("2"):

            server = threading.Thread(target=startServer)
            server.start() #starts a server thread

            return username

        elif response.startswith("3"):
        
            return username

        elif response.startswith("4"):

            addQuestions(username)
            return menu()

        elif response.startswith("5"):

            deleteUser(username)
            return menu()

    elif response.startswith("2"):
    
        createAccount()
        menu()

    else:
        #invalid response is given
        print("Invalid Response.")
        print("Please try again.")
        return menu()


username = menu() #username from the menu function

#tkinter initialisation
window = tk.Tk() #tkinter window
window.geometry("550x600") #window breadth and height
window.title(f"Quizz--{username}") #title of the window
window.configure(bg='#001F3F') #background colour configuration

#static variables for client
PORT = 5050 #unsed port in most systems
CLIENT = socket.gethostbyname(socket.gethostname())
#retrieves the ip address of the system
FORMAT = "utf-8"
#format for transferring between binary and standard unicode
DISCONNECT_MESSAGE = "!DISCONNECT"
ADDR = (CLIENT,PORT) #binds port and ip address

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#creates a client socket object
client.connect(ADDR)
#client connects to the port

#initial variables for questions
n = 0
dict={}
score = 0
scoreSheet = []
status = "yet to recieve" 
#flag variable when set to "yet to recieve", starts a while 
# loop which stops only when the flag variable changes to
#"recieved"

t = 10 #time in between questions is 10 seconds

def send(msg):
    '''used in sending messages to the server'''
    message = msg.encode(FORMAT)
    client.send(message)

def clientInterface():
    '''function that deals with all the messages 
    recieved from the server'''
    global n
    global question
    global correctAns
    global options
    global status
    global scoreSheet
    global score

    while True:

        message = client.recv(1024).decode(FORMAT)

        list1 = message.split("|")
        mode = list1[0]

        if mode:
            
            if mode == "Waiting for players":

                pass

            elif mode == "Multiplayer has started":

                pass

            elif mode == "Question":

                n += 1
                question = list1[1]
                options = eval(list1[2])
                correctAns = list1[3]
                status = "recieved"
                time.sleep(1)
                timeThread = threading.Thread(\
                    target=lambda : lapseTime(t))
                timeThread.start()
                statement = f"{n}. {question}"
                questionLabel.config(text=statement)

                ansOptionA.config(text=\
f"a) {returnOption(0)}",fg="#39CCCC",state="normal")

                ansOptionB.config(text=\
f"b) {returnOption(1)}",fg="#39CCCC",state="normal") 

                ansOptionC.config(text=\
f"c) {returnOption(2)}",fg="#39CCCC",state="normal")

                ansOptionD.config(text=\
f"d) {returnOption(3)}",fg="#39CCCC",state="normal")

            elif mode == "Current Score":

                scoreSheet = list1[1]
                scoreSheet = eval(scoreSheet)

                scoreLabel.config(text=\
f"|{scoreSheet[0][0]} : {scoreSheet[0][1]}|\
 |{scoreSheet[1][0]} : {scoreSheet[1][1]}|")

            elif mode == "End Game":
                
                scoreLabel.config(text=str())
                ansOptionA.destroy()
                ansOptionB.destroy()
                ansOptionC.destroy()
                ansOptionD.destroy()
                timeLabel.destroy()
                questionLabel.config(text="Game has Ended.")

def handle_queries(message):
    '''function used to handle certain initial queries
    from the server'''
    global username

    if message.startswith(("!USERNAME",)):

        send(username)
        recieveThread = threading.Thread(\
target=clientInterface) 
        recieveThread.start()
        #starts a thread for recieving 
        # messages from the server
        
        time.sleep(1)
        #this waits for one second so that the 
        # gui is loaded up before the questions arrive
        #otherwise this will result in an error

        send("!Start Game")
        #notifies the server thats the client is ready

message = client.recv(512).decode(FORMAT)#decodes the message
handle_queries(message)

def eventListener(event,ans=None):
    '''function handling an event in the tkinter user interface'''

    global n
    global question
    global correctAns
    global options
    global score

    for buttonOption in (0,1,2,3):
        changeColour(buttonOption,"#39CCCC")

    if event == "Check Answer":

        for buttonOption in (0,1,2,3):

                if dict[buttonOption] == "correct answer":

                    changeColour(buttonOption,"#2ECC40")

                else:

                    changeColour(buttonOption,"#FF851B")

        if ans == correctAns:

            score += 1
            send(f"!Update score:{score}")

        ansOptionA.config(state="disabled")
        ansOptionB.config(state="disabled")
        ansOptionC.config(state="disabled")
        ansOptionD.config(state="disabled")
            
def changeColour(buttonOption,colour):
    '''function used to change the colour of clicked buttons'''

    if buttonOption == 0:

        ansOptionA.config(disabledforeground=colour)

    elif buttonOption == 1:

        ansOptionB.config(disabledforeground=colour)

    elif buttonOption == 2:

        ansOptionC.config(disabledforeground=colour)

    elif buttonOption == 3:

        ansOptionD.config(disabledforeground=colour)

def returnOption(option):
    '''function used to return the required option
    as well as set the correct answer in a dict'''

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

def onClosing():
    '''target function that is prompted when 
    a tkinter window is closed'''

    if messagebox.askokcancel(\
"Quit", "Do you want to quit?"):

        window.destroy()#tkinter window is destroyed
        send("!DISCONNECT")
        #client lets server know 
        #that the client has disconnected
        exit() 

def lapseTime(t):
    '''target function that is prompted after a
    question is recieved, to run for 10 secs
    changing the timeLabel each second'''
    while True:
        try:

            timeLabel.config(text=f"Next Question in {t}")
            #timeLabel configuration every one second

        except:

            # runtime or _tcl.tkinter error occurs when the 
            # timeLabel is destroyed i.e when game ends
            print("Game has ended.")
            exit()

        t -= 1

        if t == -1:
            break
        
        time.sleep(1)


window.protocol("WM_DELETE_WINDOW", onClosing)

while status == "yet to recieve":
    #while loop waits for flag to change
    pass

else:
    #tkinter widgets are defined
    scoreLabel = tk.Label(window,bg='#001F3F',fg="#FFFFFF",\
font=('Verdana',14)) #used to define score
    statement = f"{n}. {question}" #question statement

    questionLabel = tk.Label(window,text=statement,\
font=('Verdana',16),bg='#001F3F',fg="#39CCCC",wraplength=480)

    ansOptionA = tk.Button(window, text=f"a) ", \
command=lambda : eventListener("Check Answer",returnOption(0)),\
padx=20,font=('Verdana',14),bg='#001F3F',fg="#39CCCC",\
wraplength=480)

    ansOptionB = tk.Button(window, text=f"b) ", \
command=lambda : eventListener("Check Answer",returnOption(1)),\
padx=20,font=('Verdana',14),bg='#001F3F',fg="#39CCCC",\
wraplength=480)

    ansOptionC = tk.Button(window, text=f"c) ", \
command=lambda : eventListener("Check Answer",returnOption(2)),\
padx=20,font=('Verdana',14),bg='#001F3F',fg="#39CCCC",\
wraplength=480)

    ansOptionD = tk.Button(window, text=f"d) ", \
command=lambda : eventListener("Check Answer",returnOption(3)),\
padx=20,font=('Verdana',14),bg='#001F3F',fg="#39CCCC",\
wraplength=480)

    timeLabel = tk.Label(window,text=str(t),\
bg='#001F3F',fg="#EFD469",font=('Verdana',14))

    timeThread = threading.Thread(target=lambda : lapseTime(t))
    timeThread.start()
    #time thread starts for the first time

    #packing of all the widgets in order
    questionLabel.pack(pady=20)
    ansOptionA.pack(pady=10)
    ansOptionB.pack(pady=10)
    ansOptionC.pack(pady=10)
    ansOptionD.pack(pady=10)
    timeLabel.pack(pady=5)
    scoreLabel.pack(pady=10)
    window.mainloop() 
    #mainloop starts the update loop for all tkinter objects