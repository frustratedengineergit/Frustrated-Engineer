from django.db import models
from froala_editor.fields import FroalaField
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = FroalaField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category)
    tags = models.ManyToManyField(Tag)
    image_url = models.URLField(blank=True)
    BACKGROUND_CHOICES = (
        ('default', 'Default'),
        ('color', 'Color'),
        ('image', 'Image'),
        ('custom_css', 'Custom CSS'),
    )
    background_choice = models.CharField(max_length=20, choices=BACKGROUND_CHOICES, default='default')
    background_color = models.CharField(max_length=7, blank=True, null=True)
    background_image_link = models.URLField(blank=True, null=True)
    custom_css = models.TextField(blank=True, null=True)


    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author.username} on "{self.post.title}"'
    
