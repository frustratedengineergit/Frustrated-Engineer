from django.contrib import admin
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import EmailMessage
from django import forms
from django.contrib.auth.models import Group, User
from django.template import Template, Context


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
        subject = obj.subject
        message = obj.message
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
            # Read and decode the HTML template
            html_content = html_template.read().decode('utf-8')

            # Create a Template object from the HTML content
            template = Template(html_content)

            # Fetch user details from the database
            user_details = User.objects.filter(email__in=recipient_emails).values('username', 'first_name', 'last_name')

            # Render HTML template with context
            context = {
                'subject': subject,
                'message': message,
                'recipient_emails': recipient_emails,
                'user_details': user_details,
            }
            rendered_html = template.render(Context(context))

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
