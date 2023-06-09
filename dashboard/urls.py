from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path("home", include('Home.urls')),
    path('update-user/', views.update_user, name='update_user'),
    path('change_password/', views.change_password, name='change_password'),
    path('blog/', include('blogs.urls')),
]
