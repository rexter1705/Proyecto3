from django.urls import path
from .views import home
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home, name='home'),
]