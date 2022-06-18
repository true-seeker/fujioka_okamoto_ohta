from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('exchange_keys', views.exchange_keys, name='exchange_keys'),
]
