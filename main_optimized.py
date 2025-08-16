#!/usr/bin/env python3
import asyncio
import logging
import sys
from pathlib import Path

# Добавляем путь к проекту
project_path = Path(__file__).parent
sys.path.insert(0, str(project_path))

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from config import BOT_TOKEN
from database.database import create_tables, check_database_connection
from handlers.registration import router as registration_router
from handlers.search import router as search_router
from handlers.requests import router as requests_router
from handlers.settings import router as settings_router
from handlers.profile import router as profile_router
from handlers.language import router as language_router
from utils.logger import setup_logger, log_bot_event, log_error

# Оптимизированная настройка логирования
logger = setup_logger("dating_bot", "INFO")

# Оптимизированные настройки бота
async def main():
    log_bot_event(logger, "Bot startup", "Starting optimized dating bot...")
    
    # Проверка подключения к БД
    if not check_database_connection():
        log_error(logger, Exception("Database connection failed"), "Database initialization")
        logger.error("Не удалось подключиться к базе данных. Проверьте настройки.")
        return

    # Создание таблиц
    try:
        create_tables()
        logger.info("✅ Таблицы базы данных созданы/проверены")
    except Exception as e:
        log_error(logger, e, "Table creation")
        logger.error(f"Ошибка при создании таблиц: {e}")

    # Инициализация бота с оптимизированными настройками
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()

    # Регистрация роутеров
    dp.include_router(registration_router)
    dp.include_router(search_router)
    dp.include_router(requests_router)
    dp.include_router(settings_router)
    dp.include_router(profile_router)
    dp.include_router(language_router)

    # Оптимизированные настройки
    try:
        log_bot_event(logger, "Bot polling", "Starting bot polling...")
        await dp.start_polling(bot, skip_updates=True)  # skip_updates=True для ускорения
    except Exception as e:
        log_error(logger, e, "Bot polling")
        logger.error(f"Ошибка при запуске бота: {e}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
    except Exception as e:
        log_error(logger, e, "Main execution")
        logger.error(f"Критическая ошибка: {e}") 