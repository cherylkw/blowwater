document.addEventListener('DOMContentLoaded', () => {

    // By default, submit button is disabled
    document.querySelector('#submit').disabled = true;

    // Enable button only if there is text in the input field
    document.querySelector('#input_msg').onkeyup = () => {
        document.querySelector('#submit').disabled = false;
    };

    // Retrieve chat messages history
    const request = new XMLHttpRequest();
    request.open("POST", "/listmessages");

    // Callback function for when request completes
    request.onload = () => {
        const data = JSON.parse(request.responseText);
        localStorage.setItem("chatid", data["chatid"])
        let i;
        for ( i=0; i<data["message"].length; i++) {
            const response = data["message"][i];

            // Used innerHTML instead of innerText to keep it raw
            let newmsg = `<strong>${response["chatname"]}</strong> > <big>${response["selection"]}</big> 
            <small>${response["time"]}</small><a href="/deletemessage/${response["chatname"]}&${response["selection"]}&${response["time"]}&${data["chatid"]}" id="deletemsg"> X </a><br>`;
            $("#messages").append(newmsg);
        }
    };
    request.send();



    // Connect to socket.IO
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    socket.on('connect', () => {

        // Press submit button and emit a 'submit message' event
        document.querySelector('button').onclick = function () {
            const selection = document.querySelector('input').value;
            this.form.reset();
            document.querySelector('#submit').disabled = true;
            socket.emit('submit message', {'selection': selection});
        };

    });

    // add the message to the chatroom chat list
    socket.on ('cast message', data => {
        if (data["chatid"] === localStorage.chatid) {
            let newmsg = `<strong>${data["chatname"]}</strong> > <big>${data["selection"]}</big> <small>${data["time"]}</small>
            <a href="/deletemessage/${data["chatname"]}&${data["selection"]}&${data["time"]}&${data["chatid"]}" id="deletemsg"> X </a><br>`;
            $("#messages").append(newmsg);
        }
    });


});
