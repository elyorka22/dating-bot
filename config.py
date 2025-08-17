import os
from dotenv import load_dotenv

load_dotenv()

# Токен бота
BOT_TOKEN = os.getenv("BOT_TOKEN", "8256818214:AAFwnmIc-pKeN8IgpkrW15B6TpUDVdS4ZKI")

# База данных
# Railway предоставляет DATABASE_URL для PostgreSQL
# Если DATABASE_URL не установлен, используем SQLite для локальной разработки
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///dating_bot.db")

# Если Railway предоставляет DATABASE_URL, но он начинается с postgres://, 
# нужно заменить на postgresql:// для SQLAlchemy
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

print(f"🔗 DATABASE_URL: {DATABASE_URL}")

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