const presenceSocket = new WebSocket('ws://' + window.location.host + '/ws/presence/');
presenceSocket.onopen = () => {
    console.log("Conectado ao WebSocket global de presença");
};

presenceSocket.onclose = () => {
    console.log("Desconectado do WebSocket global");
};

setInterval(() => {
    if (presenceSocket.readyState === WebSocket.OPEN) {
        presenceSocket.send(JSON.stringify({ type: "ping" }));
    }
}, 30000);
