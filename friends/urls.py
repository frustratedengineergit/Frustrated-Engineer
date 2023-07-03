from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search_users, name='search_users'),
    path('send_request/<int:receiver_id>/', views.send_friend_request, name='send_friend_request'),
    path('accept_request/<int:friend_request_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('remove_friend/<int:friend_id>/', views.remove_friend, name='remove_friend'),
    path('profile/<int:user_id>/', views.user_profile, name='user_profile'),
    path('received_friend_requests/', views.received_friend_requests, name='received_friend_requests'),
    path('connected-users/', views.connected_users_json, name='connected_users_json'),
    
]
