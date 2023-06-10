from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture_url = models.URLField(blank=True)
    linkedin_profile = models.URLField(max_length=200, blank=True)
    facebook_profile = models.URLField(max_length=200, blank=True)
    instagram_profile = models.URLField(max_length=200, blank=True)

    def __str__(self):
        return self.user.username
    
    
