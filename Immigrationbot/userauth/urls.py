# userauth/urls.py
from django.urls import path
from . import views  

urlpatterns = [
    path('', views.login_view, name='login'),  # URL for the login page
    path('send-login-link/', views.send_login_link, name='send_login_link'),
    path('one-time-login/<str:token>/', views.one_time_login, name='one_time_login'),
]
