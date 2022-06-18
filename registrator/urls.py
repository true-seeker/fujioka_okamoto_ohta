from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('generate_keys', views.generate_keys, name='generate_keys'),
    path('get_public_key', views.get_public_key, name='get_public_key'),
]
