"""Модуль создания моделей БД."""

from django.db import models


class Educator(models.Model):
    """Модель описывающая преподавателя."""

    first_name = models.CharField(max_length=55, verbose_name='Имя')
    last_name = models.CharField(max_length=55, verbose_name='Фамилия')
    middle_name = models.CharField(max_length=55, verbose_name='Отчество')

    def __str__(self: 'Educator') -> str:
        """Возвращает значение ФИО преподавателя."""
        return f'{self.last_name} {self.first_name} {self.middle_name}'

