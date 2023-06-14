from django.contrib.auth.models import User
from django.db import models

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

    def __str__(self):
        return self.user.username
