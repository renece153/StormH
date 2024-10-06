# userauth/views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import get_user_model, login
from django.core.mail import send_mail
from django.conf import settings
from itsdangerous import URLSafeTimedSerializer
from .models import UserEmail

# Function to generate the token
def generate_token(user_email):
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    return serializer.dumps(user_email, salt='email-confirm-salt')

# Function to confirm the token
def confirm_token(token):
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    try:
        email = serializer.loads(token, salt='email-confirm-salt', max_age=43200)  # 12 hours
    except Exception:
        return None
    return email

# Send the one-time login link via email
def send_login_link(request):
    user = request.user  # Replace with actual user object
    token = generate_token(user.email)
    login_url = f"{settings.SITE_URL}/one-time-login/{token}"
    
    # Send the email
    send_mail(
        'Your One-Time Login Link',
        f'Click the link below to log in:\n\n{login_url}\n\nThis link is valid for 12 hours and can only be used once.',
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )
    
    return HttpResponse("A login link has been sent to your email.")

# Handle one-time login
def one_time_login(request, token):
    email = confirm_token(token)
    if email:
        try:
            user = get_user_model().objects.get(email=email)
            login(request, user)
            return redirect('home')  # Redirect to home or any other page after login
        except get_user_model().DoesNotExist:
            return HttpResponse("Invalid token or user does not exist.")
    else:
        return HttpResponse("The login link is invalid or has expired.")


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        # Save the email if it doesn't already exist
        user_email, created = UserEmail.objects.get_or_create(email=email)
        
        if created:
            # Send the email with login link
            token = generate_token(user_email.email)
            login_url = f"{settings.SITE_URL}/one-time-login/{token}"

            send_mail(
                'Your One-Time Login Link',
                f'Click the link below to log in:\n\n{login_url}\n\nThis link is valid for 12 hours and can only be used once.',
                settings.DEFAULT_FROM_EMAIL,
                [user_email.email],
                fail_silently=False,
            )

            return HttpResponse("A login link has been sent to your email.")
        else:
            return HttpResponse("This email is already registered. Check your inbox for the login link.")
    
    return render(request, 'userauth/login.html')  # Render the login template
