"""Представления для приложения bot."""

import logging

from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.bot.serializers import FioSerializer, ScheduleRequestSerializer, ScheduleTeacherSeriaizer
from apps.bot.utils import get_filenames, get_fio, search_schedule_by_teacher, service

LOGGER = logging.getLogger(__name__)


class ServiceView(APIView):
    """Представление для обработки запросов на получение расписания по группе."""

    @staticmethod
    def get(request: Request) -> Response:
        """Обрабатывает GET-запросы с датой и именем группы, возвращая расписание."""
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

                return Response(result, status=status.HTTP_200_OK)

            except ValidationError as e:
                LOGGER.exception('Ошибка в функции service')
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            except Exception as ex:
                LOGGER.exception('Неожиданная ошибка в функции service')
                return Response(
                    {'error': str(ex)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ScheduleTeacherView(APIView):
    """Представление для обработки запросов на получение расписания по преподавателю."""

    @staticmethod
    def get(request: Request) -> Response:
        """Обрабатывает GET-запросы с датой и именем преподавателя, возвращая расписание."""
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
                LOGGER.exception('Ошибка в функции service')
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            except Exception as ex:
                LOGGER.exception('Неожиданная ошибка в функции service')

                return Response(
                    {'error': str(ex)},
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


class FioView(APIView):
    """"Представление для обработки команды ФИО."""

    @staticmethod
    def get(request: Request) -> Response:
        """Обрабатывает GET-запросы, возвращая нужное ФИО из модели Educators."""
        serializer = FioSerializer(data=request.query_params)
        if serializer.is_valid():
            fio = serializer.validated_data['fio']
            try:
                result = get_fio(fio)
                if result is None:
                    return Response(
                        {'error': 'No data returned from service.'},
                        status=status.HTTP_204_NO_CONTENT,
                    )
                return Response(result, status=status.HTTP_200_OK)

            except ValidationError as e:
                LOGGER.exception('Ошибка в функции service')
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            except Exception as ex:
                LOGGER.exception('Неожиданная ошибка в функции service')
                return Response(
                    {'error': str(ex)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
