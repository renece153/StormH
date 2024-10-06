# userauth/views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import get_user_model, login
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from itsdangerous import URLSafeTimedSerializer
from .models import UserEmail, ChatMessage
from .utils import *



def send_message(request):
    if request.method == 'POST':
        user_email = request.session.get('user_email')  # Get user email from session
        message_text = request.POST.get('message')

        # Ensure user email exists and message text is not empty
        if user_email and message_text:
            try:
                user_email_instance = UserEmail.objects.get(email=user_email)
                ChatMessage.objects.create(user_email=user_email_instance, message=message_text)
                return HttpResponseRedirect('/chat/')  # Redirect back to chat view
            except UserEmail.DoesNotExist:
                return HttpResponse("User not found.", status=404)
            except Exception as e:
                return HttpResponse(f"An error occurred: {str(e)}", status=500)
        else:
            return HttpResponse("Message text cannot be empty.", status=400)
    return HttpResponse("Invalid request method.", status=405)


# Handle one-time login
def one_time_login(request, token):
    email = confirm_token(token)  # Validate the token and get the email
    if email:
        try:
            # Get or create the user email in the UserEmail model
            user_email, created = UserEmail.objects.get_or_create(email=email)
            # Store the user's email in the session
            request.session['user_email'] = user_email.email
            
            # You can log in the user here if you have a user model
            # login(request, user)  # Uncomment if you have a user model
            
            return redirect('chat')  # Redirect to the chat view
        except Exception as e:
            print(f"Error retrieving user: {e}")  # Log the error
            return HttpResponse("Invalid token or user does not exist.")
    else:
        return HttpResponse("The login link is invalid or has expired.")



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


def chat_view(request):
    messages = ChatMessage.objects.all() 
    return render(request, 'userauth/chat.html', {'messages': messages})

