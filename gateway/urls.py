from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('check_token/', views.check_token, name='check_token'),
    path('password_recovery/', views.password_recovery, name='password_recovery'),
    path('password_recovery/reset/<user>/<token>/', views.password_reset, name='password_reset'),
]