#!/usr/bin/env python3
"""
Скрипт для добавления поля language в существующую базу данных
"""

import os
import sys

# Добавляем корневую директорию в путь
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.database import engine
from sqlalchemy import text

def add_language_field():
    """Добавить поле language в таблицу users"""
    
    print("🔧 Добавление поля language в таблицу users...")
    
    try:
        with engine.connect() as connection:
            # Проверяем, существует ли уже поле language
            result = connection.execute(text("PRAGMA table_info(users)"))
            columns = [row[1] for row in result.fetchall()]
            
            if 'language' in columns:
                print("✅ Поле language уже существует")
                return True
            
            # Добавляем поле language
            connection.execute(text("ALTER TABLE users ADD COLUMN language TEXT DEFAULT 'ru'"))
            connection.commit()
            
            print("✅ Поле language успешно добавлено")
            return True
            
    except Exception as e:
        print(f"❌ Ошибка при добавлении поля language: {e}")
        return False

if __name__ == "__main__":
    success = add_language_field()
    if success:
        print("\n✅ Миграция завершена успешно!")
    else:
        print("\n❌ Ошибка при выполнении миграции!")
        sys.exit(1) 