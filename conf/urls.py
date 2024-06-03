"""Маршрутизация URL для проекта Lizard Bot."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('bot.urls')),
]
