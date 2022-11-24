from django.urls import path
from django.shortcuts import render

from .views import index, view_lk, view_lk_order

urlpatterns = [
    path('', render, kwargs={'template_name': 'index.html'}, name='start_page'),
    path('index', index),
    path('lk-order', view_lk_order),
    path('lk', view_lk)
]
