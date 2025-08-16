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