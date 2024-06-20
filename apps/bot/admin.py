"""Модуль админки."""

from django.contrib import admin
from apps.bot.models import Educator

admin.site.register(Educator)
