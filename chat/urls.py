from django.urls import path
from chat.views import chat_room
urlpatterns = [
    # Other URL patterns
    path('<str:user1>@<str:user2>/', chat_room, name='chat_room'),
]
