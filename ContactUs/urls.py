from django.contrib import admin
from django.urls import path
from . import views
from .views import submit,my_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path('',views.index,name='ContactUs'),
    path('submit/', submit, name='submit'),
    path('my-view/', my_view, name='my_view'),
]
