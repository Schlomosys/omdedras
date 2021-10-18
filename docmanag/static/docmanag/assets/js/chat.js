var texbox = '<div class="d-flex justify-content-start mb-4">' +
    '<div class="img_cont_msg"></div>' +
    '<div class="msg_cotainer">{message}<span class="msg_time">{sender}, Le 8:40 AM, Today</span></div>' +
    '</div>';

function scrolltoend() {
    $('#board').stop().animate({
        scrollTop: $('#board')[0].scrollHeight
    }, 800);
}

function send(env_id, sender, receiver, message) {
    // $.post('/docmanag/api/messages/', '{"env_id": "' + env_id + '","sender": "' + sender + '", "receiver": "' + receiver + '","message": "' + message + '" }', function(data) {
    $.post('/docmanag/api/messages/' + env_id + '/' + sender + '/' + receiver + '/' + message, function(data) {
        console.log(data);
        var box = text_box.replace('{sender}', "You");
        box = box.replace('{message}', message);
        $('#board').append(box);
        scrolltoend();
    })
}

function receive() {
    $.get('/docmanag/api/messages/' + env_id + '/' + sender_id + '/' + receiver_id, function(data) {
        console.log(data);
        if (data.length !== 0) {
            for (var i = 0; i < data.length; i++) {
                console.log(data[i]);
                var box = texbox.replace('{sender}', data[i].sender);
                box = box.replace('{message}', data[i].message);
                $('#board').append(box);
                scrolltoend();
            }
        }
    })
}