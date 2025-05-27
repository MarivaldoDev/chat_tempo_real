const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
const lobbySocket = new WebSocket(
    `${protocol}://${window.location.host}/ws/lobby/`
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

    if (data.type === 'new_room') {
        const room = data.room;

        // Verifica se sala já existe
        if (document.getElementById('chat-card-' + room.name)) return;

        const newCard = document.createElement('div');
        newCard.className = 'chat-card';
        newCard.id = 'chat-card-' + room.name;

        newCard.innerHTML = `
            <h3 class="chat-title">${room.name}</h3>
            <p class="chat-description">${room.description}</p>
            <p id="user-count-${room.name}" class="chat-users">Nenhum usuário online</p>
            <a href="/chat/${room.name}/" class="btn-enter-room">Entrar na Sala</a>
        `;

        const grid = document.querySelector('.chat-grid');
        grid.appendChild(newCard);
    }
};
