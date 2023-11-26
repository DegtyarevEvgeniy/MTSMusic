from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from app.consumers import RoomConsumer

websocket_urlpatterns = [
    path('ws/service/room/<int:room_id>/', RoomConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    "websocket": URLRouter(websocket_urlpatterns),
})