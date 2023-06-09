from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import MemberDetail
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import re
from dashboard.models import UserProfile


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
            # Create User Profile
            user_profile = UserProfile.objects.create(user=user)
            user_profile.save()
            # Create member details
            member = MemberDetail.objects.create(user=user, phone=phone, email=email)
            # Set other member details as needed
            member.save()

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

    else:
        return render(request, "signup.html")
