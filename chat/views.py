from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from dashboard.models import UserProfile
from chat.models import Message

@login_required
def chat_room(request,user1,user2):
    # Retrieve the sender and receiver user profiles
    if user1 == request.user.username:
        r_username = user2
    elif user2 == request.user.username:
        r_username = user1 

    sender_profile = get_object_or_404(UserProfile, user=request.user)
    receiver_profile = get_object_or_404(UserProfile, user__username=r_username)
    room_name = generate_room_name(user1,user2)
    messages = Message.objects.filter(room=room_name)[0:25]
    
    context = {
        'sender_profile': sender_profile,
        'receiver_profile': receiver_profile,
        'room_name': room_name, 
        'messages': messages
    }
    
    return render(request, 'chat/chat_room.html', context)

def generate_room_name(user1, user2):
    usernames = sorted([user1, user2])
    room_name = f"{usernames[0]}_{usernames[1]}"
    return room_name