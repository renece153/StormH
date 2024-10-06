# userauth/views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import get_user_model, login
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from itsdangerous import URLSafeTimedSerializer
from .models import UserEmail
from .utils import *



def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        print(f"Email received from form: {email}")
        
        # Save the email if it doesn't already exist
        user_email, created = UserEmail.objects.get_or_create(email=email)
        
            # Generate token and create login URL
        token = generate_token(user_email.email)
        login_url = f"{settings.SITE_URL}/one-time-login/{token}"

        try:
                send_mail(
                    'Your One-Time Login Link',
                    f'Click the link below to log in:\n\n{login_url}\n\nThis link is valid for 12 hours and can only be used once.',
                    settings.DEFAULT_FROM_EMAIL,
                    [user_email.email],
                    fail_silently=False,
                )
                messages.success(request, "A login link has been sent to your email.")
        except Exception as e:
                messages.error(request, "There was an error sending the email. Please try again later.")
        
        else:
            messages.info(request, "Check your inbox for the login link.")
    
    return render(request, 'userauth/login.html') 