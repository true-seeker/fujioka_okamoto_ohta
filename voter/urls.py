from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path("logout/", LogoutView.as_view(), name="logout"),

    path("generate_keys", views.generate_keys, name="generate_keys"),
    path("get_key_from_ca", views.get_key_from_ca, name="get_key_from_ca"),

]
