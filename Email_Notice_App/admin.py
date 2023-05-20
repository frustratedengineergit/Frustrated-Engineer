from django.contrib import admin
from .models import EmailMessage
from .forms import EmailMessageForm
from django.core.mail import send_mail
from django.contrib.auth.models import User

class EmailMessageAdmin(admin.ModelAdmin):
    form = EmailMessageForm

    def save_model(self, request, obj, form, change):
        subject = obj.subject
        message = obj.message
        recipients = [user.email for user in User.objects.all()]  # Get all user emails

        send_mail(subject, message, 'ietcommunity2@gmail.com', recipients)  # Replace with your email address

admin.site.register(EmailMessage, EmailMessageAdmin)
