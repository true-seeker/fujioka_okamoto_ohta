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
    path("vote", views.vote, name="vote"),
    path("get_secret_key", views.get_secret_key, name="get_secret_key"),
    path("encrypt_ballot", views.encrypt_ballot, name="encrypt_ballot"),
    path("blind_sign_ballot", views.blind_sign_ballot, name="blind_sign_ballot"),
    path("sign_blind_signed_ballot", views.sign_blind_signed_ballot, name="sign_blind_signed_ballot"),
    path("send_to_registrator", views.send_to_registrator, name="send_to_registrator"),
    path("generate_mark", views.generate_mark, name="generate_mark"),

]
