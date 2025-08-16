#!/usr/bin/env python3
import asyncio
import logging
import os
import sys
from pathlib import Path
from aiohttp import web
import threading

# Добавляем путь к проекту
project_path = Path(__file__).parent
sys.path.insert(0, str(project_path))

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from config_railway import BOT_TOKEN
from database.database import create_tables, check_database_connection
from handlers.registration import router as registration_router
from handlers.search import router as search_router
from handlers.requests import router as requests_router
from handlers.settings import router as settings_router
from handlers.profile import router as profile_router
from handlers.language import router as language_router
from utils.logger import setup_logger, log_bot_event, log_error

# Настройка логирования для Railway
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Веб-сервер для healthcheck
async def healthcheck_handler(request):
    return web.Response(text="Bot is running!", status=200)

async def start_web_server():
    """Запуск веб-сервера для healthcheck"""
    app = web.Application()
    app.router.add_get('/', healthcheck_handler)
    app.router.add_get('/health', healthcheck_handler)
    
    port = int(os.environ.get("PORT", 8000))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    logger.info(f"🌐 Веб-сервер запущен на порту {port}")
    return runner

# Оптимизированные настройки бота для Railway
async def main():
    log_bot_event(logger, "Bot startup", "Starting Railway dating bot...")
    
    # Запускаем веб-сервер для healthcheck
    web_runner = await start_web_server()
    
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

    # Оптимизированные настройки для Railway
    try:
        log_bot_event(logger, "Bot polling", "Starting bot polling on Railway...")
        await dp.start_polling(
            bot, 
            skip_updates=True,  # Пропускать старые обновления
            polling_timeout=30,  # Увеличенный таймаут
            polling_limit=100    # Увеличенный лимит
        )
    except Exception as e:
        log_error(logger, e, "Bot polling")
        logger.error(f"Ошибка при запуске бота: {e}")
    finally:
        await bot.session.close()
        await web_runner.cleanup()

if __name__ == "__main__":
    try:
        # Получаем порт из переменной окружения Railway
        port = int(os.environ.get("PORT", 8000))
        logger.info(f"🚀 Запуск бота на порту {port}")
        
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
    except Exception as e:
        log_error(logger, e, "Main execution")
        logger.error(f"Критическая ошибка: {e}") 