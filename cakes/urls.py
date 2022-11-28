from django.contrib.auth.views import LogoutView
from django.shortcuts import render
from django.urls import path

from .views import index, view_lk

urlpatterns = [
    path('', render, kwargs={'template_name': 'index.html'}, name='start_page'),
    path('index', index),
    path('lk', view_lk),
    path("logout", LogoutView.as_view(), name="logout"),
]
