"""
Система логирования для продакшена
"""

import logging
import sys
from datetime import datetime
from pathlib import Path

def setup_logger(name: str = "dating_bot", log_level: str = "INFO") -> logging.Logger:
    """
    Настройка логгера для продакшена
    
    Args:
        name: Имя логгера
        log_level: Уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    Returns:
        Настроенный логгер
    """
    
    # Создаем директорию для логов
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Создаем логгер
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Очищаем существующие хендлеры
    logger.handlers.clear()
    
    # Форматтер для логов
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Хендлер для консоли
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Хендлер для файла (все логи)
    file_handler = logging.FileHandler(
        log_dir / f"{name}_{datetime.now().strftime('%Y%m%d')}.log",
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Хендлер для ошибок
    error_handler = logging.FileHandler(
        log_dir / f"{name}_errors_{datetime.now().strftime('%Y%m%d')}.log",
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    logger.addHandler(error_handler)
    
    return logger

def log_user_action(logger: logging.Logger, user_id: int, action: str, details: str = ""):
    """
    Логирование действий пользователя
    
    Args:
        logger: Логгер
        user_id: ID пользователя
        action: Действие
        details: Дополнительные детали
    """
    message = f"USER_ACTION | User {user_id} | {action}"
    if details:
        message += f" | {details}"
    logger.info(message)

def log_error(logger: logging.Logger, error: Exception, context: str = ""):
    """
    Логирование ошибок
    
    Args:
        logger: Логгер
        error: Исключение
        context: Контекст ошибки
    """
    message = f"ERROR | {context} | {type(error).__name__}: {str(error)}"
    logger.error(message, exc_info=True)

def log_bot_event(logger: logging.Logger, event: str, details: str = ""):
    """
    Логирование событий бота
    
    Args:
        logger: Логгер
        event: Событие
        details: Дополнительные детали
    """
    message = f"BOT_EVENT | {event}"
    if details:
        message += f" | {details}"
    logger.info(message)

def log_database_operation(logger: logging.Logger, operation: str, table: str, details: str = ""):
    """
    Логирование операций с базой данных
    
    Args:
        logger: Логгер
        operation: Операция (SELECT, INSERT, UPDATE, DELETE)
        table: Таблица
        details: Дополнительные детали
    """
    message = f"DB_OPERATION | {operation} | Table: {table}"
    if details:
        message += f" | {details}"
    logger.debug(message) 