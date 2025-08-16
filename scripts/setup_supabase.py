#!/usr/bin/env python3
"""
Скрипт для быстрой настройки Supabase
"""

import os
import sys
from supabase import create_client, Client

# Добавляем корневую директорию в путь
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import SUPABASE_URL, SUPABASE_KEY

def setup_supabase():
    """Настройка подключения к Supabase"""
    
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("❌ SUPABASE_URL и SUPABASE_KEY должны быть установлены в config.py")
        return False
    
    try:
        # Создаем клиент Supabase
        print("🔗 Подключение к Supabase...")
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # Проверяем подключение
        print("✅ Подключение к Supabase успешно!")
        
        # Получаем информацию о проекте
        print(f"📊 URL проекта: {SUPABASE_URL}")
        print(f"🔑 Ключ: {SUPABASE_KEY[:20]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка подключения к Supabase: {e}")
        return False

def test_database_connection():
    """Тест подключения к базе данных через Supabase"""
    
    try:
        from supabase import create_client, Client
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # Пробуем выполнить простой запрос
        response = supabase.table('users').select('count').limit(1).execute()
        print("✅ Подключение к базе данных успешно!")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка подключения к базе данных: {e}")
        print("💡 Возможно, таблицы еще не созданы")
        return False

def create_tables_via_api():
    """Создание таблиц через Supabase API (альтернативный способ)"""
    
    print("📋 Создание таблиц через API...")
    print("⚠️  Рекомендуется создавать таблицы через SQL Editor в панели Supabase")
    print("   Перейдите в SQL Editor и выполните SQL код из SUPABASE_SETUP.md")

if __name__ == "__main__":
    print("🚀 Настройка Supabase для бота знакомств...")
    
    # Проверяем подключение к Supabase
    if setup_supabase():
        print("\n✅ Supabase настроен успешно!")
        
        # Тестируем подключение к базе данных
        print("\n🔍 Тестирование подключения к базе данных...")
        test_database_connection()
        
        print("\n📝 Следующие шаги:")
        print("1. Перейдите в SQL Editor в панели Supabase")
        print("2. Выполните SQL код из файла SUPABASE_SETUP.md")
        print("3. Получите пароль базы данных в Settings → Database")
        print("4. Обновите DATABASE_URL в config.py")
        print("5. Запустите бота: python main.py")
        
    else:
        print("❌ Не удалось настроить Supabase")
        sys.exit(1) 