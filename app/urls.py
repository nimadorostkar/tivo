from django.urls import path, re_path
from app import views
from .views import items, profile, contact, search, favs, items_detail

app_name='app'

urlpatterns = [
    # The home page
    path('', views.index, name='home'),
    # etc
    path('profile', views.profile, name='profile'),
    path('contact', views.contact, name='contact'),
    path('search',views.search,name='search'),
]
