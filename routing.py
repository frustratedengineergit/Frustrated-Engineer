from django.urls import re_path
from chat.consumers import consumers

websocket_urlpatterns = [
    re_path(r'dashboard/ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
]
