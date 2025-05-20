const lobbySocket = new WebSocket(
    'ws://' + window.location.host + '/ws/lobby/'
);

lobbySocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    const room = data.room;
    const count = data.count;

    const userCountElement = document.getElementById('user-count-' + room);
    if (userCountElement) {
        if (count === 0) {
            userCountElement.textContent = 'Nenhum usuário online';
        } else {
            userCountElement.textContent = `🟢 ${count} usuário${count > 1 ? 's' : ''} online`;
        }
    }
};
