"""
ASGI config for snake_multiplayer project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import apps.game_engine.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'snake_multiplayer.settings')

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AuthMiddlewareStack(
        URLRouter(
            apps.game_engine.routing.websocket_urlpatters
        )
    ),
})
