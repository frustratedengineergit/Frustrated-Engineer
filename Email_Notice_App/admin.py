from django.contrib import admin
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import EmailMessage
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

    use_html_template = forms.BooleanField(label='Use HTML Template', required=False)

    html_template = forms.FileField(label='HTML Template', required=False)

    class Meta:
        model = EmailMessage
        fields = '__all__'


class EmailMessageAdmin(admin.ModelAdmin):
    form = EmailMessageAdminForm
    list_display = ('subject',)

    def save_model(self, request, obj, form, change):
        subject = form.cleaned_data.get('subject')
        message = form.cleaned_data.get('message')
        group = form.cleaned_data.get('group')
        users = form.cleaned_data.get('users')
        use_html_template = form.cleaned_data.get('use_html_template')
        html_template = form.cleaned_data.get('html_template')

        recipient_emails = []

        if group:
            recipients = group.user_set.all()
            recipient_emails.extend(user.email for user in recipients)

        if users:
            recipient_emails.extend(user.email for user in users)

        if not recipient_emails:
            recipient_emails = User.objects.values_list('email', flat=True)

        if use_html_template and html_template:
            with html_template.open() as file:
                # Read and decode the HTML template file
                html_content = file.read().decode('utf-8')

            # Render HTML template with context
            context = {
                'subject': subject,
                'message': message,
                'recipient_emails': recipient_emails,
                
            }
            rendered_html = render_to_string(html_template.name, context)

            # Generate plain text content from HTML
            text_content = strip_tags(rendered_html)

            # Send email with HTML content
            email = EmailMultiAlternatives(subject, text_content, 'communityfrustratedengineer@gmail.com', recipient_emails)
            email.attach_alternative(rendered_html, "text/html")
            email.send()
        else:
            # Send plain text email
            email = EmailMultiAlternatives(subject, message, 'communityfrustratedengineer@gmail.com', recipient_emails)
            email.send()

        obj.save()


admin.site.register(EmailMessage, EmailMessageAdmin)
