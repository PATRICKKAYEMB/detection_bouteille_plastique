import os
from django.core.asgi import get_asgi_application
from channels.security.websocket import AllowedHostsOriginValidator 
from channels.routing import ProtocolTypeRouter, URLRouter

from bouteille_app.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bouteille_detection_project.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})



