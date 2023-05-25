from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import MemberDetail
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import re


def success(request):
    return render(request, "index.html")


def signup(request):
    if request.method == "POST":
        name = request.POST["name"]
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        countryCode = request.POST["countryCode"]
        phone = request.POST["phone"]

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
                "error_message": "Username should only contain letters, numbers, and underscore (_).",
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
                username=username, email=email, password=password
            )
            user.first_name = name
            user.save()

            # Create member details
            member = MemberDetail(user=user, phone=phone, email=email)
            # Set other member details as needed
            member.save()

            # Send a welcome email
            subject = 'Welcome to Frustrated Engineers'
            from_email = 'ietcommunity2@gmail.com'
            to_email = email

            # Load the email template
            html_content = render_to_string('email_templates/Signup_Email.html')

            # Create the EmailMultiAlternatives object
            email = EmailMultiAlternatives(subject, '', from_email, [to_email])

            # Attach the HTML content
            email.attach_alternative(html_content, 'text/html')

            # Send the email
            email.send()

            # Log in the user
            user = authenticate(username=username, password=password)
            login(request, user)

            return redirect("success")  # Redirect to a home page

        except ValidationError as e:
            if "username" in e.message_dict:
                error_message = (
                    "** Username already exists. Please choose a different username. **"
                )
            else:
                error_message = "An error occurred. Please try again."

            context = {
                "error_message": error_message,
                "name": name,
                "email": email,
                "countryCode": countryCode,
                "phone": phone,
            }
            return render(request, "signup.html", context)

        except IntegrityError:
            error_message = (
                "** Username already exists. Please choose a different username. **"
            )
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
