from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from chatApp import routing

application = ProtocolTypeRouter({
    'websocket' : AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    )   
})