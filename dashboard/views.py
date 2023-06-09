from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage


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
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            if len(password) < 8:
                raise forms.ValidationError("Password must be at least 8 characters long.")
            return make_password(password)
        return self.instance.password

    def clean_profile_picture(self):
        profile_picture = self.cleaned_data.get('profile_picture')
        if profile_picture:
            # Save the profile picture to Firebase storage and get the public URL
            profile_picture_url = save_profile_picture(profile_picture)
            self.instance.userprofile.profile_picture_url = profile_picture_url

        return profile_picture

    def save(self, commit=True):
        user = super().save(commit=False)
        for field_name in self.changed_data:
            field_value = getattr(self.instance, field_name)
            setattr(user, field_name, field_value)
        if commit:
            user.save()
            user.userprofile.save()
        return user


def save_profile_picture(profile_picture):

    bucket = storage.bucket('frustratedengineer-9a5cc.appspot.com')
    filename = f"profile_pictures/{profile_picture.name}"
    blob = bucket.blob(filename)
    blob.upload_from_file(profile_picture.file)

    # Make the uploaded image publicly accessible
    blob.make_public()

    # Return the public URL of the image
    return blob.public_url
