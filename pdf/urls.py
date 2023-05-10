from django.contrib import admin
from django.urls import path
from django.conf import settings
from .views import file_list, edit, upload_file
from . import views

urlpatterns = [
    path('upload_file', views.upload_file, name='upload_file'),
    path('login/repositorio', views.file_list, name='repositorio'),
    path('post/editar/<int:pk>', views.edit, name='edit'), ]