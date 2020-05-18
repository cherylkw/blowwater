# Blow Water - Online messaging app

Web Programming with Python and JavaScript

## Welcome to Blow Water

It is an online messaging service using Flask, similar in spirit to **Slack**. You will be able to sign into this site with a display name, create channels (i.e. chatrooms) to communicate in, as well as see and join existing channels. Once a channel is selected, you will be able to send and receive messages with one another in real time. 

- **Display Name**: When a user visits the app for the first time, they should be prompted to type in a display name that will eventually be associated with every message the user sends. If a user closes the page and returns to your app later, the display name should still be remembered.
- **Channel Creation**: Any user should be able to create a new channel, so long as its name doesn’t conflict with the name of an existing channel.
- **Channel List**: Users should be able to see a list of all current channels, and selecting one should allow the user to view the channel. We leave it to you to decide how to display such a list.
- **Messages View**: Once a channel is selected, the user should see any messages that have already been sent in that channel, up to a maximum of 100 messages. Your app should only store the 100 most recent messages per channel in server-side memory.
- **Sending Messages**: Once in a channel, users should be able to send text messages to others the channel. When a user sends a message, their display name and the timestamp of the message should be associated with the message. All users in the channel should then see the new message (with display name and timestamp) appear on their channel page. Sending and receiving messages should NOT require reloading the page.
- **Remembering the Channel**: If a user is on a channel page, closes the web browser window, and goes back to your web application, your application should remember what channel the user was on previously and take the user back to that channel.
- **Personal touch** : Users can delete their own message. 
- **Personal touch** : Users cannot send blank message. Send button disable when nothing enter in the chat box.

## Functions functionality in application.py

- index() : front page
- logout() : logout the app, user information in session will be deleted
- chatroomlist() : create or load a chatroom list which created by user, use session to store the display name
- chatroom(chatid) : load the chatroom which is selected by user
- deletemessage(chatname,selection,time,chatid) : delete a specific message by it's owner and refresh the chatroom screen
- listmessages() : return list of chat in a chatroom
- message(data) : store and cast a message by **socket.IO**
- submit_channel(data) : create and cast a channel by **socket.IO**

## HTML

- index.html : front page
- layout.html : layout for all html
- error.html : display error message when error occurs
- chatroomlist.html : display list of chatroom users created
- chatroom.html : chatroom where users enter their messages

## JavaScript 

- chatroom.js : functions which perform real time data transfer between client and server using SocketIO , chat history are stored by local storage
- chatroomlist.js : functions to create channels for users and store the lists by using session

## Youtube Demo :

https://youtu.be/0QYxQm4rtDY

## Pre-requisites and programs used versions

-  Python 3.6 or higher
-  the latest version of pip

## Setting up the development environment

1. git clone this project

2. Run **pip3 install -r requirements.txt** in your terminal window to make sure that all of the necessary Python packages (Flask and Flask-SocketIO, for instance) are installed.

3. Set the environment variable **FLASK_APP** to be application.py. On a Mac or on Linux, the command to do this is export FLASK_APP=application.py. On Windows, the command is instead set FLASK_APP=application.py.

4. Run flask run to start up your Flask application.

## Visiting an URL and interact with the application

- Open the localhost http://127.0.0.1:5000/ to run the app

Author : Cheryl Kwong  Contact : cherylkwong@gmail.com