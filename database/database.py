from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from config import DATABASE_URL

# Создаем движок базы данных
# Поддерживает как SQLite, так и PostgreSQL
engine = create_engine(
    DATABASE_URL, 
    echo=True,
    # Дополнительные настройки для PostgreSQL
    pool_pre_ping=True,  # Проверка соединения перед использованием
    pool_recycle=300,    # Пересоздание соединений каждые 5 минут
)

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
    from database.models import Base
    Base.metadata.create_all(bind=engine)

def check_database_connection():
    """Проверить подключение к базе данных"""
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✅ Подключение к базе данных успешно!")
            return True
    except Exception as e:
        print(f"❌ Ошибка подключения к базе данных: {e}")
        return False 