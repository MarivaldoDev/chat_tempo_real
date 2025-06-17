# 💬 Chat em Tempo Real com Django, WebSocket e Redis

Este é um projeto de chat em tempo real desenvolvido com **Django** e **Django Channels**, utilizando **WebSocket** para comunicação bidirecional e **Redis** como backend para canais. O sistema é funcional, responsivo e pronto para produção, com foco em desempenho e interatividade.

---

## 🚀 Funcionalidades

- 🔄 Envio e recebimento de mensagens em tempo real
- 💬 Suporte a múltiplas salas de conversa
- 👥 Detecção e exibição de usuários online
- 🖼️ Upload de imagem de perfil via CDN (Cloudinary ou ImageKit)
- ✏️ Edição e exclusão de mensagens na interface
- 🔐 Autenticação integrada com o WebSocket
- 📦 Estrutura pronta para deploy (Railway ou outra plataforma ASGI)

---

## 🛠️ Tecnologias Utilizadas

- **Backend:** Django, Django Channels, ASGI, Daphne
- **Tempo real:** WebSocket, Redis (como Channel Layer)
- **Banco de dados:** PostgreSQL
- **Frontend:** HTML, CSS, JavaScript Vanilla
- **CDN de imagens:** Cloudinary / ImageKit
- **Ambiente de produção:** Railway (ou compatível)

---

## ⚙️ Como Executar Localmente

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/chat-realtime-django.git
   cd chat-realtime-django

2. Crie e ative um ambiente virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/macOS
    venv\Scripts\activate     # Windows

3. Instale as dependências:
    ```bash
    pip install -r requirements.txt

4. Configure o .env com suas variáveis (Redis, banco de dados, CDN, etc.).

5. Aplique as migrações:
    ```bash
    python3 manage.py migrate # Linux/macOS
    python manage.py migrate # Windows

6. Inicie o servidor:
    ```bash
    python3 manage.py runserver # Linux/macOS
    python manage.py runserver # Windows

---

## 📸 Pré - visualização
![Image](https://github.com/user-attachments/assets/fc7627f4-a307-42e2-8c7f-1206b4cdff33)
