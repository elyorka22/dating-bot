#!/usr/bin/env python3
"""
Скрипт для создания таблиц в Supabase через SQL
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Добавляем корневую директорию в путь
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import DATABASE_URL

def create_tables_in_supabase():
    """Создание таблиц в Supabase PostgreSQL"""
    
    # Проверяем, что используется PostgreSQL
    if not DATABASE_URL.startswith('postgresql'):
        print("❌ DATABASE_URL должен указывать на PostgreSQL")
        print("Установите переменную окружения DATABASE_URL для Supabase")
        return False
    
    try:
        # Подключаемся к PostgreSQL
        print("🔗 Подключение к PostgreSQL...")
        engine = create_engine(DATABASE_URL)
        
        # Проверяем подключение
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Подключение к PostgreSQL успешно!")
        
        # SQL код для создания таблиц
        create_tables_sql = """
        -- ========================================
        -- СОЗДАНИЕ ТАБЛИЦ ДЛЯ БОТА ЗНАКОМСТВ
        -- ========================================

        -- 1. Таблица пользователей
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            telegram_id BIGINT UNIQUE NOT NULL,
            username VARCHAR(255),
            gender VARCHAR(50) NOT NULL,
            age INTEGER NOT NULL,
            height INTEGER NOT NULL,
            weight INTEGER NOT NULL,
            marital_status VARCHAR(100) NOT NULL,
            interests TEXT,
            bio TEXT,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- 2. Таблица настроек поиска
        CREATE TABLE IF NOT EXISTS search_settings (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            gender_preference VARCHAR(50) NOT NULL,
            min_age INTEGER NOT NULL,
            max_age INTEGER NOT NULL,
            min_height INTEGER NOT NULL,
            max_height INTEGER NOT NULL,
            min_weight INTEGER NOT NULL,
            max_weight INTEGER NOT NULL,
            marital_status_preference TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- 3. Таблица запросов на доступ
        CREATE TABLE IF NOT EXISTS access_requests (
            id SERIAL PRIMARY KEY,
            from_user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            to_user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            status VARCHAR(20) DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- 4. Таблица разрешенных контактов
        CREATE TABLE IF NOT EXISTS allowed_contacts (
            id SERIAL PRIMARY KEY,
            user1_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            user2_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user1_id, user2_id)
        );
        """
        
        # Выполняем SQL код
        print("📋 Создание таблиц...")
        with engine.connect() as conn:
            conn.execute(text(create_tables_sql))
            conn.commit()
        
        print("✅ Таблицы созданы успешно!")
        
        # Создаем индексы
        create_indexes_sql = """
        -- ========================================
        -- СОЗДАНИЕ ИНДЕКСОВ ДЛЯ ОПТИМИЗАЦИИ
        -- ========================================

        -- Индексы для таблицы users
        CREATE INDEX IF NOT EXISTS idx_users_telegram_id ON users(telegram_id);
        CREATE INDEX IF NOT EXISTS idx_users_gender ON users(gender);
        CREATE INDEX IF NOT EXISTS idx_users_age ON users(age);
        CREATE INDEX IF NOT EXISTS idx_users_height ON users(height);
        CREATE INDEX IF NOT EXISTS idx_users_weight ON users(weight);
        CREATE INDEX IF NOT EXISTS idx_users_marital_status ON users(marital_status);
        CREATE INDEX IF NOT EXISTS idx_users_active ON users(is_active);
        CREATE INDEX IF NOT EXISTS idx_users_created_at ON users(created_at);

        -- Индексы для таблицы search_settings
        CREATE INDEX IF NOT EXISTS idx_search_settings_user_id ON search_settings(user_id);
        CREATE INDEX IF NOT EXISTS idx_search_settings_gender_pref ON search_settings(gender_preference);

        -- Индексы для таблицы access_requests
        CREATE INDEX IF NOT EXISTS idx_access_requests_status ON access_requests(status);
        CREATE INDEX IF NOT EXISTS idx_access_requests_from_user ON access_requests(from_user_id);
        CREATE INDEX IF NOT EXISTS idx_access_requests_to_user ON access_requests(to_user_id);
        CREATE INDEX IF NOT EXISTS idx_access_requests_created_at ON access_requests(created_at);

        -- Индексы для таблицы allowed_contacts
        CREATE INDEX IF NOT EXISTS idx_allowed_contacts_user1 ON allowed_contacts(user1_id);
        CREATE INDEX IF NOT EXISTS idx_allowed_contacts_user2 ON allowed_contacts(user2_id);
        """
        
        print("📊 Создание индексов...")
        with engine.connect() as conn:
            conn.execute(text(create_indexes_sql))
            conn.commit()
        
        print("✅ Индексы созданы успешно!")
        
        # Создаем ограничения
        create_constraints_sql = """
        -- ========================================
        -- СОЗДАНИЕ ОГРАНИЧЕНИЙ (CONSTRAINTS)
        -- ========================================

        -- Ограничения для возраста
        ALTER TABLE users ADD CONSTRAINT IF NOT EXISTS check_age_range 
            CHECK (age >= 18 AND age <= 100);

        -- Ограничения для роста
        ALTER TABLE users ADD CONSTRAINT IF NOT EXISTS check_height_range 
            CHECK (height >= 140 AND height <= 220);

        -- Ограничения для веса
        ALTER TABLE users ADD CONSTRAINT IF NOT EXISTS check_weight_range 
            CHECK (weight >= 40 AND weight <= 200);

        -- Ограничения для пола
        ALTER TABLE users ADD CONSTRAINT IF NOT EXISTS check_gender 
            CHECK (gender IN ('Мужчина', 'Женщина'));

        -- Ограничения для семейного положения
        ALTER TABLE users ADD CONSTRAINT IF NOT EXISTS check_marital_status 
            CHECK (marital_status IN ('Холост/Не замужем', 'Женат/Замужем', 'Разведен/Разведена'));

        -- Ограничения для настроек поиска
        ALTER TABLE search_settings ADD CONSTRAINT IF NOT EXISTS check_search_age_range 
            CHECK (min_age >= 18 AND max_age <= 100 AND min_age <= max_age);

        ALTER TABLE search_settings ADD CONSTRAINT IF NOT EXISTS check_search_height_range 
            CHECK (min_height >= 140 AND max_height <= 220 AND min_height <= max_height);

        ALTER TABLE search_settings ADD CONSTRAINT IF NOT EXISTS check_search_weight_range 
            CHECK (min_weight >= 40 AND max_weight <= 200 AND min_weight <= max_weight);

        ALTER TABLE search_settings ADD CONSTRAINT IF NOT EXISTS check_gender_preference 
            CHECK (gender_preference IN ('Мужчины', 'Женщины', 'Все'));

        -- Ограничения для статуса запросов
        ALTER TABLE access_requests ADD CONSTRAINT IF NOT EXISTS check_request_status 
            CHECK (status IN ('pending', 'accepted', 'rejected'));
        """
        
        print("🔒 Создание ограничений...")
        with engine.connect() as conn:
            conn.execute(text(create_constraints_sql))
            conn.commit()
        
        print("✅ Ограничения созданы успешно!")
        
        # Проверяем созданные таблицы
        print("\n📋 Проверка созданных таблиц...")
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT 
                    table_name,
                    table_type
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                    AND table_name IN ('users', 'search_settings', 'access_requests', 'allowed_contacts')
                ORDER BY table_name;
            """))
            
            tables = result.fetchall()
            for table in tables:
                print(f"  ✅ {table[0]}")
        
        print("\n🎉 Все таблицы созданы успешно!")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при создании таблиц: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Создание таблиц в Supabase PostgreSQL...")
    success = create_tables_in_supabase()
    if success:
        print("✅ Таблицы созданы успешно!")
    else:
        print("❌ Создание таблиц не удалось!")
        sys.exit(1) 