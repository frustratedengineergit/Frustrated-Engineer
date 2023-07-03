from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from blogs.models import BlogPost
from .models import FriendRequest
from dashboard.models import Friendship
from dashboard.models import UserProfile
from django.http import JsonResponse
from django.contrib import messages
from django import forms
from django.db.models import Q


@login_required
def search_users(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        results = User.objects.filter(username__icontains=query)
        data = [{'username': result.username,'user_id':result.id,'name': result.first_name + ' ' + result.last_name, 'profile_image': result.userprofile.profile_picture_url} for result in results]
        return JsonResponse(data, safe=False)
    return redirect('home')


@login_required
def received_friend_requests(request):
    received_requests = FriendRequest.objects.filter(receiver=request.user)
    data = [
        {
            'friend_request_id': request.id,
            'sender_username': request.sender.username,
            'sender_user_id': request.sender.id,
            'sender_name': request.sender.first_name + ' ' + request.sender.last_name,
            'sender_profile_image': request.sender.userprofile.profile_picture_url
        }
        for request in received_requests if not request.accepted
    ]
    return JsonResponse(data, safe=False)


@login_required
def connected_users_json(request):
    connected_users = get_connected_users(request.user.userprofile)

    users_data = []
    for friend in connected_users:
        user_data = {
            'profile_picture_url': friend.profile_picture_url,
            'first_name': friend.user.first_name,
            'last_name': friend.user.last_name,
            'user_id': friend.user.id,
        }
        users_data.append(user_data)

    return JsonResponse(users_data, safe=False)


@login_required
def send_friend_request(request, receiver_id):
    if request.method == 'POST':
        sender = request.user
        receiver = User.objects.get(id=receiver_id)
        friend_request = FriendRequest.objects.create(sender=sender, receiver=receiver)
        friend_request.save()
        return redirect('user_profile', receiver_id)
    return redirect('home')


@login_required
def accept_friend_request(request, friend_request_id):
    if request.method == 'POST':
        friend_request = FriendRequest.objects.get(id=friend_request_id)
        friend_request.accepted = True
        friend_request.save()

        sender_profile = UserProfile.objects.get(user=friend_request.sender)
        receiver_profile = UserProfile.objects.get(user=friend_request.receiver)

        Friendship.objects.create(from_user=sender_profile, to_user=receiver_profile)
        return redirect('user_profile', request.user.id)
    return redirect('home')


@login_required
def remove_friend(request, friend_id):
    if request.method == 'POST':
        friendship = Friendship.objects.filter(users__id=friend_id)
        friendship.delete()
        return redirect('user_profile', request.user.id)
    return redirect('home')


class FriendRequestForm(forms.Form):
    pass


@login_required
def user_profile(request, user_id):
    profile_user = get_object_or_404(UserProfile, user_id=user_id)
    posts = BlogPost.objects.all()
    try:
        friend_request = FriendRequest.objects.get(sender=request.user, receiver=profile_user.user)
        friend_request_sent = True
    except ObjectDoesNotExist:
        friend_request_sent = False

    # Retrieve connected users (friends)
    connected_users = get_connected_users(request.user.userprofile)

    # Check if the viewing user is a friend
    is_friend = False
    for friend in connected_users:
        if friend == profile_user :
            is_friend = True
            break

    # Handle friend request form submission
    if request.method == 'POST':
        friend_request_form = FriendRequestForm(request.POST)
        if friend_request_form.is_valid():
            friend_request = FriendRequest()
            friend_request.sender = request.user
            friend_request.receiver = profile_user.user
            friend_request.save()
            messages.success(request, 'Friend request sent successfully.')
            return redirect('user_profile', user_id=user_id)
    else:
        friend_request_form = FriendRequestForm()

    # Retrieve friend request status
    friend_request = FriendRequest.objects.filter(sender=request.user, receiver=profile_user.user).first()
    friend_request_status = ''
    if friend_request:
        friend_request_status = 'sent' if friend_request.accepted else 'pending'


    context = {
        'profile_user': profile_user,
        'is_friend': is_friend,
        'friend_request_sent': friend_request_sent,
        'friend_request_form': friend_request_form,
        'friend_request_status': friend_request_status,
        'connected_users': connected_users,
        'posts': posts,
    }
    return render(request, 'user_profile.html', context)


def get_connected_users(user_profile):
    connected_users = []
    friend_profiles = Friendship.objects.filter(Q(from_user=user_profile) | Q(to_user=user_profile))
    for friendship in friend_profiles:
        if friendship.from_user != user_profile:
            connected_users.append(friendship.from_user)
        else:
            connected_users.append(friendship.to_user)
    return connected_users
