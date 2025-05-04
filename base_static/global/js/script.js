const input = document.getElementById('input');
const messages = document.getElementById('messages');
const sendBtn = document.getElementById('sendBtn');
const onlineCount = document.getElementById('online-count');  // 👈 novo
const sound = document.getElementById('notification-sound');
const typingIndicator = document.getElementById('typing-indicator'); // 👈 adicionado

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
      onlineCount.textContent = `🟢 ${data.count - 1} usuário${data.count > 1 ? 's' : ''} online`;
    }
    return;
  }

  if (data.type === 'typing') {
    showTypingIndicator(data.username);
    return;
  }

  if (data.type === 'stop_typing') {
    hideTypingIndicator();
    return;
  }

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

  const profileImg = `<img src="${data.image_profile}" class="profile-img" alt="${data.username}">`;
  const usernameLink = `<a href="/myprofile/${data.username}/" class="chat-username"><strong>${data.username}</strong></a>`;

  msgDiv.innerHTML = `
    <div class="user-info">
      ${profileImg}
      ${usernameLink}
    </div>
    <p>${data.message}</p>
  `;

  messages.appendChild(msgDiv);
  messages.scrollTop = messages.scrollHeight;
};

chatSocket.onclose = () => console.error('❌ WebSocket fechado');
chatSocket.onerror = (e) => console.error('❌ Erro no WebSocket', e);

function sendMessage() {
  const text = input.value.trim();
  if (!text || chatSocket.readyState !== WebSocket.OPEN) return;

  chatSocket.send(JSON.stringify({ message: text }));
  input.value = '';
}

input.addEventListener("keydown", e => e.key === "Enter" && sendMessage());
sendBtn.addEventListener("click", sendMessage);

// 👉 Adição da lógica de "digitando..."
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
  if (username === undefined || username === null || username === "") return;
  typingIndicator.textContent = `${username} está digitando...`;
  typingIndicator.style.display = "block";
}

function hideTypingIndicator() {
  typingIndicator.textContent = "";
  typingIndicator.style.display = "none";
}

// mantém seus links de perfil
document.addEventListener("click", (e) => {
  const el = e.target.closest(".chat-username");
  if (el) {
    const username = el.textContent.replace('@', '').trim();
    if (username) {
      window.location.href = `/myprofile/${username}/`;
    }
  }
});