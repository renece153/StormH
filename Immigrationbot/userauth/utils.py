from itsdangerous import URLSafeTimedSerializer
from django.conf import settings

def generate_token(user_email):
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    return serializer.dumps(user_email, salt='email-confirm-salt')

def confirm_token(token, expiration=43200):  # 12 hours = 43200 seconds
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    try:
        email = serializer.loads(token, salt='email-confirm-salt', max_age=expiration)
    except Exception as e:
        return False
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
