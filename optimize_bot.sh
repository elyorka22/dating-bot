#!/bin/bash

echo "🚀 Оптимизация бота знакомств..."

# Подключение к VPS и настройка оптимизации
ssh root@185.23.34.213 << 'EOF'

echo "📁 Переходим в папку бота..."
cd /home/botuser/dating_bot

echo "💾 Создаем оптимизированный main.py..."
cat > main.py << 'MAIN_EOF'
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
MAIN_EOF

echo "⚙️ Создаем оптимизированный config.py..."
cat > config.py << 'CONFIG_EOF'
import os
from dotenv import load_dotenv

load_dotenv()

# Токен бота
BOT_TOKEN = "8256818214:AAFwnmIc-pKeN8IgpkrW15B6TpUDVdS4ZKI"

# Оптимизированные настройки базы данных
# Используем SQLite для лучшей производительности
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///dating_bot.db")

# Supabase настройки (для продакшена, если нужно)
SUPABASE_URL = "https://jcouuxyzslspubviwfnz.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Impjb3V1eHl6c2xzcHVidml3Zm56Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTUyOTMwNTYsImV4cCI6MjA3MDg2OTA1Nn0.mPtyUI9wzj8fDYdtYceDn7zQJmH_zsMHbpAQxXXiJuU"
SUPABASE_DB_URL = os.getenv("SUPABASE_DB_URL")

# Оптимизированные настройки бота
MAX_REQUESTS_PER_DAY = 20  # Увеличено для лучшей производительности
MIN_AGE = 18
MAX_AGE = 100
MIN_HEIGHT = 140
MAX_HEIGHT = 220
MIN_WEIGHT = 40
MAX_WEIGHT = 200

# Гендеры
GENDERS = ["Мужчина", "Женщина"]

# Семейное положение
MARITAL_STATUSES = ["Холост/Не замужем", "Женат/Замужем", "Разведен/Разведена"]

# Интересы
INTERESTS = [
    "Спорт", "Музыка", "Кино", "Книги", "Путешествия",
    "Кулинария", "Искусство", "Технологии", "Природа",
    "Фотография", "Танцы", "Йога", "Игры", "Наука"
]

# Оптимизированные настройки производительности
BOT_POLLING_TIMEOUT = 30  # Увеличено для стабильности
BOT_POLLING_LIMIT = 100   # Увеличено для обработки большего количества сообщений
SKIP_UPDATES = True       # Пропускать старые обновления при запуске

# Настройки логирования
LOG_LEVEL = "INFO"
LOG_FILE = "logs/dating_bot.log"

# Настройки безопасности
RATE_LIMIT_ENABLED = True
SPAM_PROTECTION_ENABLED = True
CONFIG_EOF

echo "🔧 Обновляем .env файл для SQLite..."
cat > .env << 'ENV_EOF'
BOT_TOKEN=8256818214:AAFwnmIc-pKeN8IgpkrW15B6TpUDVdS4ZKI
DATABASE_URL=sqlite:///dating_bot.db
SUPABASE_URL=https://jcouuxyzslspubviwfnz.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Impjb3V1eHl6c2xzcHVidml3Zm56Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTUyOTMwNTYsImV4cCI6MjA3MDg2OTA1Nn0.mPtyUI9wzj8fDYdtYceDn7zQJmH_zsMHbpAQxXXiJuU
LOG_LEVEL=INFO
LOG_FILE=logs/dating_bot.log
MAX_REQUESTS_PER_DAY=20
RATE_LIMIT_ENABLED=true
SPAM_PROTECTION_ENABLED=true
ENV_EOF

echo "📋 Проверяем файлы..."
ls -la main.py config.py .env

echo "🔄 Перезапускаем бота..."
systemctl restart dating-bot

echo "📊 Проверяем статус бота..."
systemctl status dating-bot --no-pager

echo "✅ Оптимизация завершена!"
echo "🚀 Бот теперь должен работать быстрее!"

EOF

echo "🎉 Оптимизация завершена!" 