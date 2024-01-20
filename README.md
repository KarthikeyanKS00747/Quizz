# Quizz - A Quiz-Based Learning Platform

## Acknowledgement

I would like to express my sincere gratitude to **Ms. Fouzia Salma**, our Computer Science teacher, for her dedicated teaching and support throughout this project. Special thanks to our Head Teacher, **Monika Sethi**, for her encouragement and inspiration. I also extend my gratitude to my teachers, parents, and fellow students for their valuable contributions.

## Preface

This project serves as practical experience in coding various programs for daily life use. In the wake of the global pandemic, our lifestyle has shifted significantly, with online classes causing stress among students. This project aims to provide a solution to enhance the learning experience during these challenging times.

## Introduction

The **COVID-19 pandemic** has brought about significant changes in our lifestyle, with online classes becoming the norm. This shift has led to challenges in learning and focus during classes, impacting students' exam preparations. The program presented here assists students in studying for exams by randomizing answer options, promoting active recall.

## Objective

The primary goal of this project is to alleviate the stress caused by the pandemic on students. The program facilitates exam preparation in a fun and enjoyable manner by allowing students to input questions and answers. The randomized options prevent memorization of patterns, promoting a deeper understanding of the material.

## Scope

The project envisions revolutionizing learning through active recall, with future plans for online competitions and communication features. The system aims to create a supportive learning environment, encouraging students to participate in collaborative learning activities.

## Existing System

In the existing system, users must read various resources, memorize theory, and create questions manually. Carrying around unclassified information is inconvenient, and identifying challenging questions requires trial and error.

## Proposed System

The proposed system streamlines the process by allowing users to input questions directly, randomizing options, and enabling multiple players to engage through a server. It provides a structured and classified approach to learning, making it easier for users to revise and prepare for exams.

# Quiz Application Structure

## File Structure

The quiz application is organized into major segments split into subfiles for modularity and clarity. The key files include:

1. **LocalServer.py**
   - Contains the local server implementation.
   - Imported as a separate thread when a multiplayer game is prompted.
   
2. **SinglePlayer.py**
   - Handles the single-player functionality.
   - Incorporates menu options, user account management, and question handling.

3. **Questions.txt**
   - A text file containing a single-line string of a dictionary.
   - The dictionary includes questions, answers, and usernames in a list.

## Quiz File Overview

The main quiz file serves as the central hub for the application, encompassing the following features:

- **Menu:**
  - Presents options for database operations, user account management, and question handling.

- **Database Operations:**
  - Creation of new user accounts.
  - Logging into existing accounts.
  - Deleting existing accounts.

- **Question Handling:**
  - Functionality for adding questions to the text file.

- **Client-Side Aspect:**
  - Integrates the client-side aspect of the application.

## Multiplayer Game Flow

- **Local Server Integration:**
  - When a multiplayer game is prompted, the `LocalServer.py` file is imported as a separate thread to start a local server.
  
- **Host and User Connection:**
  - The host joins the server and waits for the second user to join.
  - Upon a user joining, their username is requested, and a player object is created on the server, storing socket object and IP address information.

- **Thread Creation:**
  - Threads are created in both the server and the client for handling requests and messages when connected.

- **Game Initiation:**
  - Once two users are connected, a broadcasted message informs both users that the game has begun.
  - The server sends the first question.

- **Time Management:**
  - A time thread is initiated, counting down from 10 seconds after a question is broadcasted from the server.

- **GUI Creation:**
  - A new tkinter window and widgets are created on both clients.
  - The window displays the question, options, and a timer.

This structured approach ensures a clear separation of concerns and allows for efficient management of different aspects of the quiz application.


## Input Requirements

**From the Administrator:**
1. Create a username "Admin" with a password.
2. Log in using the created credentials.

**From the User:**
1. Create a username with a password.
2. Log in using the provided credentials.

## Output Requirements

**For Administrator:**
- Singleplayer Start Game
- Multiplayer Start Game
- Multiplayer Join Game
- Add Questions
- Delete Users

**For Users:**
- Singleplayer Start Game
- Multiplayer Start Game
- Multiplayer Join Game
- Add Questions

## Hardware/Software Requirements

**Hardware:**
- Computer system
- RAM: at least 2GB (4GB preferable)
- Storage: Minimum 1 GB

**Software:**
- Python 3.7 Shell
- Windows 7 and above or Mac OS X 10.11
- MySQL database with the following commands:
  - `CREATE DATABASE Quiz;`
  - `CREATE TABLE LoginData(ID INTEGER PRIMARY KEY AUTO_INCREMENT, Username VARCHAR(50), Password VARCHAR(255));`
  - `ALTER TABLE LoginData AUTO_INCREMENT=100;`
