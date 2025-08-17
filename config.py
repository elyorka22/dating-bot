import os
from dotenv import load_dotenv

load_dotenv()

# Токен бота
BOT_TOKEN = os.getenv("BOT_TOKEN", "8256818214:AAFwnmIc-pKeN8IgpkrW15B6TpUDVdS4ZKI")

# База данных
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///dating_bot.db")

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