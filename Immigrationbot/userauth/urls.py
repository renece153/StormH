# userauth/urls.py
from django.urls import path
from . import views  

urlpatterns = [
    path('', views.login_view, name='login'),  # URL for the login page
    path('chat/', views.chat_view, name='chat'), 
    path('send-message/', views.send_message, name='send_message'),
    path('one-time-login/<str:token>/', views.one_time_login, name='one_time_login'),
]
