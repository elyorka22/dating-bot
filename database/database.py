from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from config import DATABASE_URL
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создаем движок базы данных
# Поддерживает как SQLite, так и PostgreSQL
if DATABASE_URL.startswith("postgresql://"):
    # Настройки для PostgreSQL (Railway)
    engine = create_engine(
        DATABASE_URL, 
        echo=True,
        pool_pre_ping=True,  # Проверка соединения перед использованием
        pool_recycle=300,    # Пересоздание соединений каждые 5 минут
        pool_size=10,        # Размер пула соединений
        max_overflow=20,     # Максимальное количество дополнительных соединений
        connect_args={
            "connect_timeout": 10,  # Таймаут подключения
            "application_name": "dating_bot"  # Имя приложения
        }
    )
    logger.info("🔗 Подключение к PostgreSQL (Railway)")
else:
    # Настройки для SQLite (локальная разработка)
    engine = create_engine(
        DATABASE_URL, 
        echo=True,
        connect_args={"check_same_thread": False}
    )
    logger.info("🔗 Подключение к SQLite (локальная разработка)")

# Создаем фабрику сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
Base = declarative_base()

def get_db() -> Session:
    """Получить сессию базы данных"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """Создать все таблицы в базе данных"""
    try:
        from database.models import Base
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Таблицы созданы успешно")
    except Exception as e:
        logger.error(f"❌ Ошибка создания таблиц: {e}")
        raise

def check_database_connection():
    """Проверить подключение к базе данных"""
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            logger.info("✅ Подключение к базе данных успешно!")
            return True
    except Exception as e:
        logger.error(f"❌ Ошибка подключения к базе данных: {e}")
        return False 