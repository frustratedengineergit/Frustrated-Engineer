from authentication import views as auth_views
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', auth_views.signup, name='signup'),
    path('success/', views.success, name='success'),
    
]
