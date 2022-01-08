from django.urls import path, re_path
from app import views
from .views import profile, contact

app_name='app'

urlpatterns = [
    # The home page
    path('', views.index, name='home'),
    # etc
    path('profile', views.profile, name='profile'),
    path('contact', views.contact, name='contact'),
    path('about', views.about, name='about'),
]
