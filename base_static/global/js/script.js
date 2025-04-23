const input = document.getElementById('input');
const messages = document.getElementById('messages');
const sendBtn = document.getElementById('sendBtn');

const roomName = document.body.dataset.room || "sala123";
const currentUserId = parseInt(document.body.dataset.userId);

const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
const chatSocket = new WebSocket(
  `${protocol}://${window.location.host}/ws/chat/${roomName}/`
);

chatSocket.onopen = function () {
  console.log('✅ Conectado ao WebSocket');
  sendBtn.disabled = false;
};

chatSocket.onmessage = function (e) {
  const data = JSON.parse(e.data);

  const msgDiv = document.createElement('div');
  msgDiv.className = 'message';

  if (data.user_id === currentUserId) {
    msgDiv.classList.add('user');
  } else {
    msgDiv.classList.add('bot');
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

  const userDiv = document.createElement('div');
  messages.appendChild(userDiv);
  messages.scrollTop = messages.scrollHeight;

  chatSocket.send(JSON.stringify({ message: text }));
  input.value = '';
}

input.addEventListener("keydown", e => e.key === "Enter" && sendMessage());
sendBtn.addEventListener("click", sendMessage);

document.addEventListener("click", (e) => {
  const el = e.target.closest(".chat-username");
  if (el) {
    const username = el.textContent.replace('@', '').trim();
    if (username) {
      window.location.href = `/myprofile/${username}/`;
    }
  }
});
