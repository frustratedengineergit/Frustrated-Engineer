from django.contrib import admin
from django.urls import path
from . import views
from .views import submit

urlpatterns = [
    path("admin/", admin.site.urls),
    path('',views.index,name='ContactUs'),
    path('submit/', submit, name='submit'),
]
