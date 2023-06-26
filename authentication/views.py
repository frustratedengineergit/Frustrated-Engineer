import random
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.core.mail import EmailMultiAlternatives,send_mail
from django.template.loader import render_to_string
import re
from dashboard.models import UserProfile
from django.contrib.sites.shortcuts import get_current_site
from django_otp.util import random_hex
from django.contrib.auth.forms import SetPasswordForm
from django_otp import oath
from django.db import DatabaseError

def success(request):
    return render(request, "index.html")


def signup(request):
    if request.method == "POST":
        name = request.POST.get("name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        countryCode = request.POST.get("countryCode")
        phone = request.POST.get("phone")

        # Validate username
        if len(username) > 15:
            context = {
                "error_message": "Username should be less than or equal to 15 characters.",
                "name": name,
                "email": email,
                "countryCode": countryCode,
                "phone": phone,
            }
            return render(request, "signup.html", context)

        if not re.match(r"^[a-zA-Z0-9_]+$", username):
            context = {
                "error_message": "Username should only contain letters, numbers, and underscores (_).",
                "name": name,
                "email": email,
                "countryCode": countryCode,
                "phone": phone,
            }
            return render(request, "signup.html", context)

        if username.startswith("_"):
            context = {
                "error_message": "Username should not start with an underscore (_).",
                "name": name,
                "email": email,
                "countryCode": countryCode,
                "phone": phone,
            }
            return render(request, "signup.html", context)

        try:
            # Check if email already exists
            if User.objects.filter(email=email).exists():
                context = {
                    "error_message": "Email already exists. Please choose a different email.",
                    "name": name,
                    "username": username,
                    "countryCode": countryCode,
                    "phone": phone,
                }
                return render(request, "signup.html", context)
        
            # Create the user
            user = User.objects.create_user(
                username=username, email=email, password=password, first_name=name
            )
            #Generating a Default Profile Picture Url for future updates.
            url_profile = 'https://media.tenor.com/aNVkfUVH1GsAAAAd/gif.gif'
            # Create User Profile
            user_profile = UserProfile.objects.create(user=user,phone_number=phone,profile_picture_url=url_profile)
            user_profile.save()

            # Send a welcome email
            subject = 'Welcome to Frustrated Engineers'
            from_email = 'communityfrustratedengineer@gmail.com'
            to_email = email

            # Load the email template
            context = {'first_name': name}
            html_content = render_to_string('email_templates/Signup_Email.html', context)

            # Create the EmailMultiAlternatives object
            email = EmailMultiAlternatives(subject, body=html_content, from_email=from_email, to=[to_email])
            email.content_subtype = 'html'

            # Attach the HTML content
            email.attach_alternative(html_content, 'text/html')

            # Send the email
            email.send()

            # Log in the user
            user = authenticate(request, username=username, password=password)
            login(request, user)

            return redirect("success")  # Redirect to the home page

        except ValidationError as e:
            error_message = "An error occurred. Please try again."

            if "username" in e.message_dict:
                error_message = "Username already exists. Please choose a different username."

            context = {
                "error_message": error_message,
                "name": name,
                "email": email,
                "countryCode": countryCode,
                "phone": phone,
            }
            return render(request, "signup.html", context)

        except IntegrityError:
            error_message = "Username already exists. Please choose a different username."

            context = {
                "error_message": error_message,
                "name": name,
                "email": email,
                "countryCode": countryCode,
                "phone": phone,
            }
            return render(request, "signup.html", context)
        
        except DatabaseError as e:
            context = {
            "error_message": "Username or Email already exists. Please choose a different one.",
            "name": name,
            "username": username,
            "countryCode": countryCode,
            "phone": phone,
            }
            return render(request, "signup.html", context)
    else:
        return render(request, "signup.html")
def generate_otp():
    return random.randint(100000, 999999)

def reset_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)

            # Generate OTP
            otp = generate_otp()
            # Save the OTP to the user's session or database
            request.session['otp'] = otp

            # Render the email template
            email_context = {
                'user': user,
                'domain': get_current_site(request).domain,
                'otp': otp
            }
            message = render_to_string('email_templates/reset_password_otp_email.html', email_context)

            # Send OTP to the user's email
            mail_subject = 'Reset Your Password - OTP'
            sender_email = 'communityfrustratedengineer@gmail.com'
            recipient_email = [email]
            send_mail(mail_subject, message, sender_email, recipient_email, html_message=message)

            print(otp)

            return redirect('verify_otp')
        except User.DoesNotExist:
            return render(request, 'reset_password.html', {'error': 'User does not exist.'})

    return render(request, 'reset_password.html')


def verify_otp(request):
    if request.method == 'POST':
        user_otp = request.POST.get('otp')
        stored_otp = request.session.get('otp')
        
        if user_otp == str(stored_otp):
            return redirect('password_reset')
        else:
            return render(request, 'verify_otp.html', {'error': 'Invalid OTP'})
    return render(request, 'verify_otp.html')

def password_reset(request):
    if request.method == 'POST':
        form = SetPasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'password_reset_success.html')
    else:
        form = SetPasswordForm(request.user)
    return render(request, 'password_reset.html', {'form': form})


# To be Deleted, Only for Developement Purpose

def password_reset_success(request):
    return render(request, 'password_reset_success.html')