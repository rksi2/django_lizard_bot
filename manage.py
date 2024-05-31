
"""Утилита командной строки Django для административных задач."""

import os
import sys


class DjangoImportError(ImportError):
    """Ошибка импорта Django."""

    def __init__(self: '__init__') -> None:
        """Инициализация    импорта Django."""
        super().__init__(
            'Не удалось импортировать Django. Убедитесь, что он установлен и '
            'доступен в вашей переменной окружения PYTHONPATH. Возможно, вы '
            'забыли активировать виртуальное окружение?',
        )


def main() -> None:
    """Выполнение административных задач."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lizard_bot.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise DjangoImportError from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
