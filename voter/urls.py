from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path("logout/", LogoutView.as_view(), name="logout"),
]
