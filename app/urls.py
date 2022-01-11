from django.urls import path, re_path
from app import views
from django.contrib.auth.views import LogoutView


app_name='app'

urlpatterns = [
    path('', views.index, name='home'),
    path('contact', views.contact, name='contact'),
    path('about', views.about, name='about'),
    path('request', views.request, name='request'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('profile', views.profile, name='profile'),
    path('logout', LogoutView.as_view(), name="logout"),
    path('password_change/', views.password_change, name="password_change"),
    path('checkout/<int:id>/', views.checkout, name="checkout"),
]
