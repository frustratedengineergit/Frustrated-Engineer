from authentication import views as auth_views
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('signup/', auth_views.signup, name='signup'),
    path('success/', views.success, name='success'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('password-reset/', views.password_reset, name='password_reset'),

    # for developement purpose only delete everything below in production
    path('password-reset/success', views.password_reset_success, name='password_reset_success'),
    
    
]
