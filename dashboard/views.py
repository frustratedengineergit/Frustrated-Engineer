from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from .models import UserProfile
from django.contrib.auth import update_session_auth_hash

@login_required
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

@login_required
def update_user(request):
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('dashboard')
    else:
        form = UpdateUserForm(instance=request.user)
    return render(request, 'dashboard/update_user.html', {'form': form})

class UpdateUserForm(UserChangeForm):
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
    
    def clean_profile_picture(self):
        profile_picture = self.cleaned_data.get('profile_picture')
        if profile_picture:
            # Save the profile picture to Firebase storage and get the public URL
            profile_picture_url = save_profile_picture(profile_picture)
            user_profile = UserProfile.objects.get(user=self.instance)
            user_profile.profile_picture_url = profile_picture_url
            user_profile.save()

        return profile_picture

def save_profile_picture(profile_picture):
    bucket = storage.bucket('frustratedengineer-9a5cc.appspot.com')
    filename = f"profile_pictures/{profile_picture.name}"
    blob = bucket.blob(filename)
    blob.upload_from_file(profile_picture.file)

    # Make the uploaded image publicly accessible
    blob.make_public()

    # Return the public URL of the image
    return blob.public_url

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Update the session with the user's new password
            messages.success(request, 'Your password has been changed.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'dashboard/change_password.html', {'form': form})

