# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('password-reset/', views.password_reset_request, name='password_reset'),
    path('password-reset/otp/', views.password_reset_otp, name='password_reset_otp'),
]
