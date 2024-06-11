"""Маршрутизация URL для приложения bot."""

from django.urls import path

from apps.bot.views import FileListView, FioView, ScheduleTeacherView, ServiceView

urlpatterns = [
    path('files/', FileListView.as_view(), name='file-list'),
    path('fio/', FioView.as_view(), name='fio'),
    path('service/', ServiceView.as_view(), name='service'),
    path('teachers/', ScheduleTeacherView.as_view(), name='teacher'),
]
