import os
from dotenv import load_dotenv

load_dotenv()

# Токен бота
BOT_TOKEN = "8256818214:AAFwnmIc-pKeN8IgpkrW15B6TpUDVdS4ZKI"

# Настройки базы данных
# Для локальной разработки используем SQLite
# Для продакшена - Supabase PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///dating_bot.db")

# Supabase настройки (для продакшена)
SUPABASE_URL = "https://jcouuxyzslspubviwfnz.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Impjb3V1eHl6c2xzcHVidml3Zm56Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTUyOTMwNTYsImV4cCI6MjA3MDg2OTA1Nn0.mPtyUI9wzj8fDYdtYceDn7zQJmH_zsMHbpAQxXXiJuU"
SUPABASE_DB_URL = os.getenv("SUPABASE_DB_URL")  # PostgreSQL connection string

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