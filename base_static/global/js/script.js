const input = document.getElementById('input');
const messages = document.getElementById('messages');
const sendBtn = document.getElementById('sendBtn');
const onlineCount = document.getElementById('online-count');
const sound = document.getElementById('notification-sound');
const typingIndicator = document.getElementById('typing-indicator');

let typingTimer;
const TYPING_INTERVAL = 1000;

const roomName = document.body.dataset.room || "sala123";
const currentUserId = parseInt(document.body.dataset.userId);

const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
const chatSocket = new WebSocket(
  `${protocol}://${window.location.host}/ws/chat/${roomName}/`
);

chatSocket.onopen = function () {
  console.log('✅ Conectado ao WebSocket');
  if (sendBtn) sendBtn.disabled = false;
};

chatSocket.onmessage = function (e) {
  const data = JSON.parse(e.data);

  if (data.type === 'online_count') {
    if (onlineCount) {
      const onlineUsers = data.count - 1;
      onlineCount.textContent = `🟢 ${onlineUsers} usuário${onlineUsers === 1 ? '' : 's'} online`;
    }
    return;
  }

  if (data.type === 'typing') {
    if (data.user_id !== currentUserId) {
      showTypingIndicator(data.username);
    }
    return;
  }

  if (data.type === 'stop_typing') {
    if (data.user_id !== currentUserId) {
      hideTypingIndicator();
    }
    return;
  }

  if (data.type === "chat_message") {
    const msgDiv = document.createElement('div');
    msgDiv.className = 'message';
  
    if (data.user_id === currentUserId) {
      msgDiv.classList.add('user');
    } else {
      msgDiv.classList.add('bot');
      if (sound && chatSocket.readyState === WebSocket.OPEN) {
        sound.play().catch(err => console.error('Erro ao tocar som:', err));
      }
    }
  
    const username = data.username || "Usuário";
    const profileImg = `<img src="${data.image_profile}" class="profile-img" alt="${username}">`;
    const usernameLink = data.username
      ? `<a href="/myprofile/${username}/" class="chat-username"><strong>${username}</strong></a>`
      : `<strong>${username}</strong>`;

    const hora = data.timestamp
    ? new Date(data.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    : "";
  
    msgDiv.innerHTML = `
      <div class="user-info">
        ${profileImg}
        ${usernameLink}
        <span class="timestamp">${hora}</span>
      </div>
      <p>${data.message}</p>
    `;
  
    messages.appendChild(msgDiv);
    messages.scrollTop = messages.scrollHeight;
  }
};

chatSocket.onclose = () => console.error('❌ WebSocket fechado');
chatSocket.onerror = (e) => console.error('❌ Erro no WebSocket', e);

function sendMessage() {
  const text = input.value.trim();
  if (!text || chatSocket.readyState !== WebSocket.OPEN) return;

  chatSocket.send(JSON.stringify({ message: text }));
  input.value = '';
}

// Previne comportamento padrão do Enter (evita recarregar página)
input.addEventListener("keydown", e => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

sendBtn.addEventListener("click", sendMessage);

// Detecção de digitação
input.addEventListener("input", () => {
  clearTimeout(typingTimer);

  chatSocket.send(JSON.stringify({
    type: "typing"
  }));

  typingTimer = setTimeout(() => {
    chatSocket.send(JSON.stringify({
      type: "stop_typing"
    }));
  }, TYPING_INTERVAL);
});

function showTypingIndicator(username) {
  if (!username) return;
  typingIndicator.textContent = `${username} está digitando...`;
  typingIndicator.style.display = "block";
}

function hideTypingIndicator() {
  typingIndicator.textContent = "";
  typingIndicator.style.display = "none";
}
