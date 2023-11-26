from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from app.consumers import RoomConsumer, RoomTrackTimeConsumer

application = ProtocolTypeRouter({
    "websocket": URLRouter(
        [
            path("ws/rooms/<int:room_id>/", RoomConsumer.as_asgi()),
            path("ws/rooms/<int:room_id>/get_track_time/", RoomTrackTimeConsumer.as_asgi()),
        ]
    ),
})