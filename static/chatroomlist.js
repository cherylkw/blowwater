document.addEventListener('DOMContentLoaded', () => {

    // Connect to socket.IO
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    socket.on('connect', () => {

        // click button to trigger a 'submit channel' event
        document.querySelector('form button').onclick = () => {
            const selection = document.querySelector('form input').value;
            socket.emit('submit channel', {'selection': selection})
        };
    });

    //afer created channel, update and broadcast an updated channel list
    socket.on ('cast channel', data => {
        const li = document.createElement('li');

        li.innerHTML = `<a href="/chatrooms/${data["chatid"]}"> ${data["selection"]} </a>`;
        console.log(li.innerHTML);
        document.querySelector('#chatrooms').append(li);
    });
});
