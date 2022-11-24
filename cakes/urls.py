from django.urls import path

from .views import index, view_lk, view_lk_order

urlpatterns = [
    path('', index),
    path('lk-order', view_lk_order),
    path('lk', view_lk)
]
