import os

from datetime import datetime
from flask import Flask, render_template, session, request, redirect, url_for, jsonify
from flask_session import Session
from flask_socketio import SocketIO, emit

app = Flask(__name__)
# configuring session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configuring socketio
app.config["SECRET_KEY"] = "my secret key"
socketio = SocketIO(app)

chatnames = []  # display name list
chatroomlists = []  # chatroom list
messageRecord = {}  # chat messages history

# Front page
@app.route("/")
def index():
    if "chatname" in session:
         # redirect user to his/her previous chatroom before quit
        if "chatid" in session:
            if len(chatroomlists) >= session["chatid"]:
                return redirect(url_for('chatroom', chatid=session["chatid"]))

        # redirect user to his/her previous chatroom list page if not in the chatroom before
        return redirect(url_for('chatroomlist'))
    return render_template("index.html")

# Logout app
@app.route("/logout", methods=["GET"])
def logout():
    try:
        logoutname = session.pop("chatname")
    except TypeError:
        return render_template("error.html", error_message="Display name already exists.")
    else:
        chatnames.remove(logoutname)

    return redirect(url_for('index'))

# Create or loading chatroom list of a user
@app.route("/chatrooms", methods=["GET", "POST"])
def chatroomlist():

    # Check if the display name already exist, if not add to session
    if request.method == "POST":
        chatname = request.form.get("chatname")
        if chatname in chatnames:
            return render_template("error.html", error_message="Display name already exists.")
        chatnames.append(chatname)
        session["chatname"] = chatname

    # Ensure user has login
    if request.method=="GET" and "chatname" not in session:
        return render_template("error.html", error_message="Display name not found.")

    return render_template("chatroomlist.html", chatroomlists=chatroomlists, chatname=session["chatname"])

# Load the chatroom selected by user
@app.route("/chatrooms/<int:chatid>", methods=["GET", "POST"])
def chatroom(chatid):

    # Check the chatroom is on the chatroom list
    if request.method == "POST":
        chatroom_name = request.form.get("chatroom_name")
        if chatroom_name in chatroomlists:
            return render_template("error.html", error_message="The chatroom already exists.")

        # Add the new chatroom on the chatroom list
        chatroomlists.append(chatroom_name)
        messageRecord[chatroom_name] = []

    # Ensure user has login the app and chatroom is exist if loading the page by url
    if request.method == "GET":
        if "chatname" not in session:
            return render_template("error.html", error_message="No such display name exist.")
        if len(chatroomlists) < chatid:
            return render_template("error.html", error_message="Chatroom Doesn't Exist.")

    # Add id of current channel of user to his/her session
    session["chatid"] = chatid
    temp=chatroomlists[chatid-1]
    return render_template("chatroom.html", chatname=session["chatname"], chatroom_name=temp)

# Delete message by the message owner
@app.route("/deletemessage/<string:chatname>&<string:selection>&<string:time>&<int:chatid>",methods=["GET"])
def deletemessage(chatname,selection,time,chatid):
    response_dict = {"selection": selection, "time": time, "chatname": chatname}
    messagelist = messageRecord[chatroomlists[session["chatid"] - 1]]
    # Ensure user is the owner of the message
    if session["chatname"] == chatname:
        for i in range(len(messagelist)):
             # Find the message in the messagelist
             if messagelist[i] == response_dict:
                 del messagelist[i]
                 break

        session["chatid"] = chatid
        return redirect(url_for('chatroom', chatid=session["chatid"]))
    else:
        return render_template("error.html", error_message="Only owner of the message can delete this message")

# Return the list of messages of the current chatroom
@app.route("/listmessages", methods=["POST"])
def listmessages():
    return jsonify({**{"message": messageRecord[chatroomlists[session["chatid"]-1]]}, **{"chatid": session["chatid"]}})

# Socket io to broadcast the message
@socketio.on("submit message")
def message(data):
    selection = data["selection"]
    # Format current datetime
    time = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Store the message
    response_dict = {"selection": selection, "time": time, "chatname": session["chatname"]}
    messagelist = messageRecord[chatroomlists[session["chatid"] - 1]]

    # When reaching 100 of messages, delete the first message
    if len(messagelist) == 100:
        del messagelist[0]

    # Broadcase message to current channel
    messagelist.append(response_dict)
    emit("cast message", {**response_dict, **{"chatid": str(session["chatid"])}}, broadcast=True)


# Create and update channel list of a user
@socketio.on("submit channel")
def submit_channel(data):

    # Broadcast the new channel to all users
    emit("cast channel", {"selection": data["selection"], "chatid": len(chatroomlists) + 1}, broadcast=True)
    

if __name__ == "__main__":
    app.run(debug=True)

