from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture_url = models.URLField(blank=True)
    dob = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=200, blank=True)
    linkedin_profile = models.URLField(max_length=200, blank=True)
    facebook_profile = models.URLField(max_length=200, blank=True)
    instagram_profile = models.URLField(max_length=200, blank=True)

    def __str__(self):
        return self.user.username


class Education(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='educations')
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=100)
    year = models.CharField(max_length=10)

    def __str__(self):
        return self.institution


class Skill(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='skills')
    skill = models.CharField(max_length=100)

    def __str__(self):
        return self.skill
