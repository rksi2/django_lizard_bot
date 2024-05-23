"""Сериализаторы для проекта lizard_bot."""
from rest_framework import serializers


class ScheduleRequestSerializer(serializers.Serializer):
    """Сериализатор для запросов расписания по группе."""

    date = serializers.CharField()
    group = serializers.CharField()


class ScheduleTeacherSeriaizer(serializers.Serializer):
    """Сериализатор для запросов расписания по преподавателю."""

    date = serializers.CharField()
    group = serializers.CharField()
