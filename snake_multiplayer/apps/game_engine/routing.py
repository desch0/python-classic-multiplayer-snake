from django.urls import re_path
from . import consumers

websocket_urlpatters = [
    re_path(r'^ws/room$', consumers.GameDataConsumer.as_asgi())
]
