"""Frustrated_Engineer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from blogs.views import login_view, logout_view

admin.site.site_header = "Frustrated Engineer Admin"
admin.site.site_title = "Frustrated Engineer Admin Portal"
admin.site.index_title = "Welcome to the Frustrated Engineer's Admin Page"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include('Home.urls')),
    path("Features/", include('Features.urls')),
    path("Gallery/",include('Gallery.urls')),
    path("FAQ/",include('FAQ.urls')),
    path("AboutUs/",include('AboutUs.urls')),
    path("ContactUs/",include('ContactUs.urls')),
    path('signup/', include('authentication.urls')),
    path('blog/', include('blogs.urls')),
    path('accounts/login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

]