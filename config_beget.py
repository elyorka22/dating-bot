"""
Конфигурация для деплоя на Beget
"""

import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Токен бота
BOT_TOKEN = os.getenv("BOT_TOKEN", "8256818214:AAFwnmIc-pKeN8IgpkrW15B6TpUDVdS4ZKI")

# Настройки базы данных для Beget
# Для Beget лучше использовать SQLite, так как он проще в настройке
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///dating_bot.db")

# Supabase настройки (опционально)
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://jcouuxyzslspubviwfnz.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Impjb3V1eHl6c2xzcHVidml3ZnN6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTUyOTMwNTYsImV4cCI6MjA3MDg2OTA1Nn0.mPtyUI9wzj8fDYdtYceDn7zQJmH_zsMHbpAQxXXiJuU")

# Настройки бота
MAX_REQUESTS_PER_DAY = 10
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

# Настройки для Beget
BEGET_CONFIG = {
    "python_version": "3.8",
    "max_memory": "512M",
    "timeout": 300,
    "restart_on_failure": True
} 