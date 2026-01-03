"""
ASGI config for petite_detection_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

import os
from channels.security.websocket import AllowedHostsOriginValidator 
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from detection_app.routing import websocket_urlpatterns
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "petite_detection_project.settings")



application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})




