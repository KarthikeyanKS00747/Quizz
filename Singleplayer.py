from random import shuffle
from tkinter import messagebox
import tkinter as tk

#tkinter initial variables
window = tk.Tk()
window.geometry("550x600")
window.title("Quizz")
window.configure(bg='#001F3F')


def useQuestions():
    '''function used in getting questions from questions.txt'''

    with open("questions.txt", "r") as file:
        
        singleLine = file.readline()
        dict = eval(singleLine)

    return dict

def eventListener(event):
    '''function handling an event in the tkinter user interface'''

    global n
    global items
    global correctAns
    global options
    global score

    for buttonOption in (0,1,2,3):
        changeColour(buttonOption,"#39CCCC")
    
    if event == "Next Question":

        n += 1

        try:

            statement = f"{n+1}. {str(items[n][0])}"

        except IndexError:

            n = 0
            statement = f"{n+1}. {str(items[n][0])}"
        
        correctAns = items[n][1][3]
        options = items[n][1][0:4]
        shuffle(options)

        questionLabel.config(text=statement)
        
        ansOptionA.config(text=f"a) {returnOption(0)}")
        ansOptionB.config(text=f"b) {returnOption(1)}") 
        ansOptionC.config(text=f"c) {returnOption(2)}") 
        ansOptionD.config(text=f"d) {returnOption(3)}") 

    elif event == "Previous Question":

        n -= 1
        statement = f"{n+1}. {str(items[n][0])}"
        correctAns = items[n][1][3]
        options = items[n][1][0:4]
        shuffle(options)

        questionLabel.config(text=statement)

        ansOptionA.config(text=f"a) {returnOption(0)}")
        ansOptionB.config(text=f"b) {returnOption(1)}") 
        ansOptionC.config(text=f"c) {returnOption(2)}") 
        ansOptionD.config(text=f"d) {returnOption(3)}")

    elif event == "Check Answer":

        for buttonOption in (0,1,2,3):

                if dict[buttonOption] == "correct answer":

                    changeColour(buttonOption,"#2ECC40")

                else:
                    
                    changeColour(buttonOption,"#FF851B")

def changeColour(buttonOption,colour):
    '''function used to change the colour of clicked buttons'''

    if buttonOption == 0:

        ansOptionA.config(fg=colour)

    elif buttonOption == 1:

        ansOptionB.config(fg=colour)

    if buttonOption == 2:

        ansOptionC.config(fg=colour)

    if buttonOption == 3:
        
        ansOptionD.config(fg=colour)       

def returnOption(option):
    '''function used to return the required option
    as well as set the correct answer in a dict'''

    global n
    global items
    global options
    global dict

    if options[option] == correctAns:

        dict[option] = "correct answer"

    else:
        
        dict[option] = "incorrect answer"

    return options[option]

def on_closing():
    '''target function that is prompted when 
    a tkinter window is closed'''
    
    if messagebox.askokcancel(\
"Quit", "Do you want to quit?"):
        
        window.destroy()
        exit() 

window.protocol("WM_DELETE_WINDOW", on_closing)

#initial variables
dict = {}
score = 0
n = 0
dict_qs = useQuestions()
items = list(dict_qs.items())
shuffle(items)
correctAns = items[n][1][3]
options = items[n][1][0:4]
shuffle(options)

#tkinter widgets
statement = f"{n+1}. {str(items[n][0])}"
questionLabel = tk.Label(window,text=statement,\
font=('Verdana',16),bg='#001F3F',fg="#39CCCC",wraplength=480)

nextQuestion = tk.Button(window, text="Next Question", \
command=lambda : eventListener("Next Question"),\
font=('Verdana',10),bg='#001F3F',fg="#39CCCC",padx=20)

prevQuestion = tk.Button(window, text="Previous Question", \
command=lambda : eventListener("Previous Question"),\
font=('Verdana',10),bg='#001F3F',fg="#39CCCC",padx=20)

ansOptionA = tk.Button(window, text=f"a) {returnOption(0)}", \
command=lambda : eventListener("Check Answer"),padx=20,\
font=('Verdana',14),bg='#001F3F',fg="#39CCCC",wraplength=480) 

ansOptionB = tk.Button(window, text=f"b) {returnOption(1)}", \
command=lambda : eventListener("Check Answer"),padx=20,\
font=('Verdana',14),bg='#001F3F',fg="#39CCCC",wraplength=480) 

ansOptionC = tk.Button(window, text=f"c) {returnOption(2)}", \
command=lambda : eventListener("Check Answer"),padx=20,\
font=('Verdana',14),bg='#001F3F',fg="#39CCCC",wraplength=480) 

ansOptionD = tk.Button(window, text=f"d) {returnOption(3)}", \
command=lambda : eventListener("Check Answer"),padx=20,\
font=('Verdana',14),bg='#001F3F',fg="#39CCCC",wraplength=480) 

#packing of widgets
questionLabel.pack(pady=20)
nextQuestion.pack(pady=10)
prevQuestion.pack(pady=10)
ansOptionA.pack(pady=10)
ansOptionB.pack(pady=10)
ansOptionC.pack(pady=10)
ansOptionD.pack(pady=10)
window.mainloop()
