import os
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import app.routing  # use o nome do seu app com routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SEUPROJETO.settings')  # ajuste para o nome do seu projeto

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,  # ✅ isso resolve o erro
    "websocket": AuthMiddlewareStack(
        URLRouter(
            app.routing.websocket_urlpatterns
        )
    ),
})
