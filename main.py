import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
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

# Настройка логирования
logger = setup_logger("dating_bot", "INFO")

async def main():
    """Главная функция запуска бота"""
    log_bot_event(logger, "Bot startup", "Starting dating bot...")
    
    # Проверяем подключение к базе данных
    if not check_database_connection():
        log_error(logger, Exception("Database connection failed"), "Database initialization")
        logger.error("Не удалось подключиться к базе данных. Проверьте настройки.")
        return
    
    # Создаем таблицы в базе данных
    try:
        create_tables()
        log_bot_event(logger, "Database initialized", "Tables created successfully")
    except Exception as e:
        log_error(logger, e, "Table creation")
        logger.error(f"Ошибка при создании таблиц: {e}")
        return
    
    # Инициализируем бота
    try:
        bot = Bot(
            token=BOT_TOKEN,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )
        log_bot_event(logger, "Bot initialized", f"Token: {BOT_TOKEN[:10]}...")
    except Exception as e:
        log_error(logger, e, "Bot initialization")
        logger.error(f"Ошибка при инициализации бота: {e}")
        return
    
    # Создаем диспетчер
    dp = Dispatcher()
    
    # Регистрируем роутеры
    routers = [
        registration_router,
        search_router,
        requests_router,
        settings_router,
        profile_router,
        language_router
    ]
    
    for router in routers:
        dp.include_router(router)
    
    log_bot_event(logger, "Routers registered", f"Total routers: {len(routers)}")
    logger.info("Бот запущен и готов к работе!")
    
    # Запускаем бота
    try:
        log_bot_event(logger, "Starting polling", "Bot is now polling for updates")
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        log_bot_event(logger, "Bot stopped", "User interrupted")
        logger.info("Бот остановлен пользователем")
    except Exception as e:
        log_error(logger, e, "Bot polling")
        logger.error(f"Ошибка при работе бота: {e}")
    finally:
        try:
            await bot.session.close()
            log_bot_event(logger, "Bot session closed", "Cleanup completed")
        except Exception as e:
            log_error(logger, e, "Session cleanup")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        log_error(logger, e, "Main function")
        logger.critical(f"Критическая ошибка при запуске бота: {e}")
        sys.exit(1) 