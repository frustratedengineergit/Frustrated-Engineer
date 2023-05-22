from django.contrib import admin
from .models import EmailMessage
from .forms import EmailMessageForm
from django.core.mail import send_mail
from django import forms
from django.contrib.auth.models import Group, User


class EmailMessageAdminForm(forms.ModelForm):

    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'select2'}),
    )

    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'select2'}),
    )

    class Meta:
        model = EmailMessage
        fields = '__all__'

class EmailMessageAdmin(admin.ModelAdmin):
    form = EmailMessageAdminForm

    def save_model(self, request, obj, form, change):
        subject = obj.subject
        message = obj.message
        group = form.cleaned_data.get('group')
        users = form.cleaned_data.get('users')

        recipient_emails = []

        if group:
            recipients = group.user_set.all()  # Get all users in the selected group
            recipient_emails.extend(user.email for user in recipients)

        if users:
            recipient_emails.extend(user.email for user in users)

        send_mail(subject, message, 'ietcommunity2@gmail.com', recipient_emails)

        # Save the email message after sending
        obj.save()

admin.site.register(EmailMessage, EmailMessageAdmin)
