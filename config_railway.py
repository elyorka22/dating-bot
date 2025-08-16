import os
from dotenv import load_dotenv

load_dotenv()

# Токен бота из переменной окружения Railway
BOT_TOKEN = os.getenv("BOT_TOKEN", "8256818214:AAFwnmIc-pKeN8IgpkrW15B6TpUDVdS4ZKI")

# База данных из Railway (PostgreSQL)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///dating_bot.db")

# Supabase настройки (опционально)
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://jcouuxyzslspubviwfnz.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Impjb3V1eHl6c2xzcHVidml3Zm56Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTUyOTMwNTYsImV4cCI6MjA3MDg2OTA1Nn0.mPtyUI9wzj8fDYdtYceDn7zQJmH_zsMHbpAQxXXiJuU")
SUPABASE_DB_URL = os.getenv("SUPABASE_DB_URL")

# Оптимизированные настройки бота
MAX_REQUESTS_PER_DAY = int(os.getenv("MAX_REQUESTS_PER_DAY", "20"))
MIN_AGE = int(os.getenv("MIN_AGE", "18"))
MAX_AGE = int(os.getenv("MAX_AGE", "100"))
MIN_HEIGHT = int(os.getenv("MIN_HEIGHT", "140"))
MAX_HEIGHT = int(os.getenv("MAX_HEIGHT", "220"))
MIN_WEIGHT = int(os.getenv("MIN_WEIGHT", "40"))
MAX_WEIGHT = int(os.getenv("MAX_WEIGHT", "200"))

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

# Оптимизированные настройки производительности для Railway
BOT_POLLING_TIMEOUT = int(os.getenv("BOT_POLLING_TIMEOUT", "30"))
BOT_POLLING_LIMIT = int(os.getenv("BOT_POLLING_LIMIT", "100"))
SKIP_UPDATES = os.getenv("SKIP_UPDATES", "true").lower() == "true"

# Настройки логирования
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "logs/dating_bot.log")

# Настройки безопасности
RATE_LIMIT_ENABLED = os.getenv("RATE_LIMIT_ENABLED", "true").lower() == "true"
SPAM_PROTECTION_ENABLED = os.getenv("SPAM_PROTECTION_ENABLED", "true").lower() == "true"

# Railway специфичные настройки
PORT = int(os.getenv("PORT", "8000"))
ENVIRONMENT = os.getenv("ENVIRONMENT", "production") 