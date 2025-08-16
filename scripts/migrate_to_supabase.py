#!/usr/bin/env python3
"""
Скрипт для миграции данных из SQLite в Supabase PostgreSQL
"""

import os
import sys
import json
from datetime import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Добавляем корневую директорию в путь
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.models import User, SearchSettings, AccessRequest, AllowedContact
from config import DATABASE_URL

load_dotenv()

def migrate_data():
    """Мигрировать данные из SQLite в PostgreSQL"""
    
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
        
        # Создаем таблицы в PostgreSQL
        print("📋 Создание таблиц в PostgreSQL...")
        from database.models import Base
        Base.metadata.create_all(bind=engine)
        
        # Создаем сессию
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Проверяем, есть ли данные в PostgreSQL
        existing_users = db.query(User).count()
        if existing_users > 0:
            print(f"⚠️  В PostgreSQL уже есть {existing_users} пользователей")
            response = input("Продолжить миграцию? (y/N): ")
            if response.lower() != 'y':
                return False
        
        # Подключаемся к SQLite для чтения данных
        sqlite_url = "sqlite:///dating_bot.db"
        sqlite_engine = create_engine(sqlite_url)
        sqlite_SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sqlite_engine)
        sqlite_db = sqlite_SessionLocal()
        
        print("📤 Начинаем миграцию данных...")
        
        # Мигрируем пользователей
        print("👥 Миграция пользователей...")
        users = sqlite_db.query(User).all()
        for user in users:
            # Проверяем, не существует ли уже пользователь
            existing_user = db.query(User).filter(User.telegram_id == user.telegram_id).first()
            if not existing_user:
                new_user = User(
                    telegram_id=user.telegram_id,
                    username=user.username,
                    gender=user.gender,
                    age=user.age,
                    height=user.height,
                    weight=user.weight,
                    marital_status=user.marital_status,
                    interests=user.interests,
                    bio=user.bio,
                    is_active=user.is_active,
                    created_at=user.created_at,
                    updated_at=user.updated_at
                )
                db.add(new_user)
                print(f"  ✅ Пользователь {user.telegram_id} мигрирован")
            else:
                print(f"  ⚠️  Пользователь {user.telegram_id} уже существует")
        
        db.commit()
        
        # Мигрируем настройки поиска
        print("⚙️  Миграция настроек поиска...")
        search_settings = sqlite_db.query(SearchSettings).all()
        for setting in search_settings:
            # Находим пользователя в PostgreSQL
            user = db.query(User).filter(User.telegram_id == setting.user.telegram_id).first()
            if user:
                existing_setting = db.query(SearchSettings).filter(SearchSettings.user_id == user.id).first()
                if not existing_setting:
                    new_setting = SearchSettings(
                        user_id=user.id,
                        gender_preference=setting.gender_preference,
                        min_age=setting.min_age,
                        max_age=setting.max_age,
                        min_height=setting.min_height,
                        max_height=setting.max_height,
                        min_weight=setting.min_weight,
                        max_weight=setting.max_weight,
                        marital_status_preference=setting.marital_status_preference,
                        created_at=setting.created_at,
                        updated_at=setting.updated_at
                    )
                    db.add(new_setting)
                    print(f"  ✅ Настройки для пользователя {user.telegram_id} мигрированы")
        
        db.commit()
        
        # Мигрируем запросы на доступ
        print("📨 Миграция запросов на доступ...")
        access_requests = sqlite_db.query(AccessRequest).all()
        for request in access_requests:
            # Находим пользователей в PostgreSQL
            from_user = db.query(User).filter(User.telegram_id == request.from_user.telegram_id).first()
            to_user = db.query(User).filter(User.telegram_id == request.to_user.telegram_id).first()
            
            if from_user and to_user:
                existing_request = db.query(AccessRequest).filter(
                    AccessRequest.from_user_id == from_user.id,
                    AccessRequest.to_user_id == to_user.id
                ).first()
                
                if not existing_request:
                    new_request = AccessRequest(
                        from_user_id=from_user.id,
                        to_user_id=to_user.id,
                        status=request.status,
                        created_at=request.created_at,
                        updated_at=request.updated_at
                    )
                    db.add(new_request)
                    print(f"  ✅ Запрос от {from_user.telegram_id} к {to_user.telegram_id} мигрирован")
        
        db.commit()
        
        # Мигрируем разрешенные контакты
        print("🤝 Миграция разрешенных контактов...")
        allowed_contacts = sqlite_db.query(AllowedContact).all()
        for contact in allowed_contacts:
            # Находим пользователей в PostgreSQL
            user1 = db.query(User).filter(User.telegram_id == contact.user1.telegram_id).first()
            user2 = db.query(User).filter(User.telegram_id == contact.user2.telegram_id).first()
            
            if user1 and user2:
                existing_contact = db.query(AllowedContact).filter(
                    AllowedContact.user1_id == user1.id,
                    AllowedContact.user2_id == user2.id
                ).first()
                
                if not existing_contact:
                    new_contact = AllowedContact(
                        user1_id=user1.id,
                        user2_id=user2.id,
                        created_at=contact.created_at
                    )
                    db.add(new_contact)
                    print(f"  ✅ Контакт между {user1.telegram_id} и {user2.telegram_id} мигрирован")
        
        db.commit()
        
        print("🎉 Миграция завершена успешно!")
        
        # Выводим статистику
        print("\n📊 Статистика миграции:")
        print(f"  👥 Пользователей: {db.query(User).count()}")
        print(f"  ⚙️  Настроек поиска: {db.query(SearchSettings).count()}")
        print(f"  📨 Запросов на доступ: {db.query(AccessRequest).count()}")
        print(f"  🤝 Разрешенных контактов: {db.query(AllowedContact).count()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при миграции: {e}")
        return False
    finally:
        if 'db' in locals():
            db.close()
        if 'sqlite_db' in locals():
            sqlite_db.close()

if __name__ == "__main__":
    print("🚀 Запуск миграции данных в Supabase PostgreSQL...")
    success = migrate_data()
    if success:
        print("✅ Миграция завершена успешно!")
    else:
        print("❌ Миграция не удалась!")
        sys.exit(1) 