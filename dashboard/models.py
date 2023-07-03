from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth import get_user_model

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture_url = models.URLField(blank=True)
    dob = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=200, blank=True)
    bio = models.TextField(blank=True)
    linkedin_profile = models.URLField(max_length=200, blank=True)
    facebook_profile = models.URLField(max_length=200, blank=True)
    instagram_profile = models.URLField(max_length=200, blank=True)
    friends = models.ManyToManyField('UserProfile', through='Friendship', through_fields=('from_user', 'to_user'), related_name='user_friends')

    def __str__(self):
        return self.user.username

User = get_user_model()

class Friendship(models.Model):
    from_user = models.ForeignKey('UserProfile', related_name='friends_from', on_delete=models.CASCADE)
    to_user = models.ForeignKey('UserProfile', related_name='friends_to', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.from_user} - {self.to_user}'
