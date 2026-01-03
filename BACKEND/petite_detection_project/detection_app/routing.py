from .consumers import DetectorConsumer
from django.urls import re_path

websocket_urlpatterns = [
    re_path(r'ws/detect/$', DetectorConsumer.as_asgi()),
]
