from django.urls import path,include
from . import views
from routing import websocket_urlpatterns
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path("home", include('Home.urls')),
    path('update-user/', views.update_user, name='update_user'),
    path('change_password/', views.change_password, name='change_password'),
    path('blog/', include('blogs.urls')),
    path('users/', include('friends.urls')),
    path('chat/', include('chat.urls')),
]

urlpatterns += websocket_urlpatterns

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': URLRouter(websocket_urlpatterns),
})