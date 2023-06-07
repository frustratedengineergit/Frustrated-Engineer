from django.urls import path
from .views import (
    BlogPostCreateView,
    BlogPostDetailView,
    BlogPostUpdateView,
    BlogPostDeleteView,
    blog_posts,
    comment_create
)

urlpatterns = [
    path('', blog_posts, name='blog_posts'),
    path('create/', BlogPostCreateView.as_view(), name='create_blog_post'),
    path('<int:pk>/', BlogPostDetailView.as_view(), name='blog_post_detail'),
    path('<int:pk>/update/', BlogPostUpdateView.as_view(), name='update_blog_post'),
    path('<int:pk>/delete/', BlogPostDeleteView.as_view(), name='delete_blog_post'),
    path('comment/create/<int:pk>/', comment_create, name='comment_create'),

]