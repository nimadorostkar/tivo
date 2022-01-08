from django.urls import path, re_path
from app import views


app_name='app'

urlpatterns = [
    path('', views.index, name='home'),
    path('profile', views.profile, name='profile'),
    path('contact', views.contact, name='contact'),
    path('about', views.about, name='about'),
    path('request', views.request, name='request'),
]
