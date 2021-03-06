from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('check_token/', views.check_token, name='check_token'),
    path('password_recovery/', views.password_recovery, name='password_recovery'),
    path('password_recovery/reset/<user>/<token>/', views.password_reset, name='password_reset'),
    path('get_producer_supermarket/', views.get_producer_supermarket, name='get_producer_supermarket'),
    path('register_material/', views.register_material, name='register_material'),
    path('material_types/', views.material_types, name='material_types'),
    path('materials/', views.materials, name='materials_list'),
    path('register_composter/', views.register_composter, name='register_composter'),
    path('get_producer_composters/', views.get_producer_composters, name='get_producer_composters'),
    path('get_supermarket_composters/', views.get_supermarket_composters, name='get_supermarket_composters'),
    path('get_composter_alerts/', views.get_composter_alerts, name='get_composter_alerts'),
    url(r'update_material/(?P<id>[A-Za-z0-9]+)$', views.update_material, name='update_material'),
    url(r'update_composter/(?P<id>[A-Za-z0-9]+)$', views.update_composter, name='update_composter'),
    url(r'get_composter_report/(?P<id>[A-Za-z0-9]+)$', views.get_composter_report, name='get_composter_report'),
    url(r'^producers/(?P<id>[0-9]*)$', views.get_producers, name="get_producers"),
    url(r'^supermarkets/(?P<id>[0-9]*)$', views.get_supermarkets, name="get_supermarkets"),
]