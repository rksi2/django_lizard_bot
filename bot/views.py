"""Представления для приложения bot."""

import logging

from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .disk import get_filenames, search_schedule_by_teacher, service
from .serializers import ScheduleRequestSerializer, ScheduleTeacherSeriaizer

# Настройка логирования
logger = logging.getLogger(__name__)


class ServiceView(APIView):
    """Представление для обработки запросов на получение расписания по группе."""

    @staticmethod
    def get(request: Request) -> Response:
        """Обрабатывает POST-запросы с датой и именем группы, возвращая расписание."""
        logger.info(request.data)
        serializer = ScheduleRequestSerializer(data=request.query_params)
        if serializer.is_valid():
            name = serializer.validated_data['date']
            group = serializer.validated_data['group']
            try:
                result = service(name, group)
                if result is None:
                    return Response(
                        {'error': 'No data returned from service.'},
                        status=status.HTTP_204_NO_CONTENT,
                    )
                logger.info(result)
                return Response(result, status=status.HTTP_200_OK)
            except ValidationError as e:
                # Логирование ошибки
                logger.exception('Ошибка в функции service')
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            except Exception:
                # Логирование ошибки с трассировкой стека
                logger.exception('Неожиданная ошибка в функции service')
                return Response(
                    {'error': 'Internal server error.'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        logger.error(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ScheduleTeacherView(APIView):
    """Представление для обработки запросов на получение расписания по преподавателю."""

    @staticmethod
    def get(request: Request) -> Response:
        """Обрабатывает POST-запросы с датой и именем преподавателя, возвращая расписание."""
        serializer = ScheduleTeacherSeriaizer(data=request.query_params)
        if serializer.is_valid():
            date = serializer.validated_data['date']
            teachers_name = serializer.validated_data['group']
            try:
                result = search_schedule_by_teacher(date, teachers_name)
                if result is None:
                    return Response(
                        {'error': 'No data returned from service.'},
                        status=status.HTTP_204_NO_CONTENT,
                    )
                return Response(result, status=status.HTTP_200_OK)
            except ValidationError as e:
                # Логирование ошибки
                logger.exception('Ошибка в функции service')
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            except Exception:
                # Логирование ошибки с трассировкой стека
                logger.exception('Неожиданная ошибка в функции service')
                return Response(
                    {'error': 'Internal server error.'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FileListView(APIView):
    """Представление для получения списка файлов."""

    @staticmethod
    def get(request: Request) -> Response:
        """Обрабатывает GET-запросы, возвращая список файлов с Google Drive."""
        files = get_filenames()
        return Response(files)
