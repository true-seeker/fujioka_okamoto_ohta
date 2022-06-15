from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('registrator/', include('registrator.urls')),
    path('certification_authority/', include('certification_authority.urls')),
    path('vote_counter/', include('vote_counter.urls')),
    path('voter/', include('voter.urls')),
    # path('', views.index),
    path('admin/', admin.site.urls),
]
