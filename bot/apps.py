"""Конфигурация приложения bot для проекта lizard_bot."""

from django.apps import AppConfig


class BotConfig(AppConfig):
    """Конфигурационный класс для приложения бота в проекте Lizard Bot."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bot'
