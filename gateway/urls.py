from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('check_token/', views.check_token, name='check_token'),
    path('password_recovery/', views.password_recovery, name='password_recovery'),
    path('password_recovery/reset/<user>/<token>/', views.password_reset, name='password_reset'),
    path('register_material/', views.register_material, name='register_material'),
    path('material_types/', views.material_types, name='material_types'),
    url(r'^producers/(?P<id>[0-9]*)$', views.get_producers, name="get_producers"),
]