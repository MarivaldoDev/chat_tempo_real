const input = document.getElementById('input');
const messages = document.getElementById('messages');
const sendBtn = document.getElementById('sendBtn');
const userId = Math.random().toString(36).substring(2, 10);
const roomName = document.body.dataset.room;  // se estiver usando data-room no HTML

const chatSocket = new WebSocket(
  'ws://' + window.location.host + '/ws/chat/' + roomName + '/'
);

chatSocket.onopen = function () {
  console.log('✅ Conectado ao WebSocket');
  sendBtn.disabled = false;
};

chatSocket.onmessage = function (e) {
  const data = JSON.parse(e.data);

  if (data.sender === userId) return; // ignora mensagens que já foram renderizadas localmente

  const msgDiv = document.createElement('div');
  msgDiv.className = 'message bot'; // visual do "outro usuário"
  msgDiv.textContent = data.message;

  messages.appendChild(msgDiv);
  messages.scrollTop = messages.scrollHeight;
};

chatSocket.onclose = () => console.error('❌ WebSocket fechado');
chatSocket.onerror = (e) => console.error('❌ Erro no WebSocket', e);

function sendMessage() {
  const text = input.value.trim();
  if (!text || chatSocket.readyState !== WebSocket.OPEN) return;

  // Mostra localmente (estilo do "user")
  const userDiv = document.createElement('div');
  userDiv.className = 'message user';
  userDiv.textContent = text;
  messages.appendChild(userDiv);
  messages.scrollTop = messages.scrollHeight;

  // Envia para o grupo
  chatSocket.send(JSON.stringify({
    message: text,
    sender: userId
  }));

  input.value = '';
}

input.addEventListener("keydown", e => e.key === "Enter" && sendMessage());
sendBtn.addEventListener("click", sendMessage);
