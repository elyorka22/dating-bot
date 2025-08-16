#!/usr/bin/env python3
"""
Скрипт для тестирования Supabase API
"""

import os
import sys

# Добавляем корневую директорию в путь
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.supabase_adapter import SupabaseAdapter

def test_supabase_api():
    """Тестирование Supabase API"""
    
    print("🚀 Тестирование Supabase API...")
    
    try:
        # Создаем адаптер
        adapter = SupabaseAdapter()
        print("✅ Supabase адаптер создан")
        
        # Тестируем подключение
        print("\n🔍 Тестирование подключения...")
        
        # Пробуем получить список пользователей
        response = adapter.supabase.table('users').select('count').limit(1).execute()
        print("✅ Подключение к таблице users успешно!")
        
        # Проверяем количество пользователей
        users_count = len(response.data) if response.data else 0
        print(f"📊 Количество пользователей в базе: {users_count}")
        
        # Тестируем создание тестового пользователя
        print("\n👤 Тестирование создания пользователя...")
        test_user_data = {
            'telegram_id': 999999999,
            'username': 'test_user',
            'gender': 'Мужчина',
            'age': 25,
            'height': 175,
            'weight': 70,
            'marital_status': 'Холост/Не замужем',
            'interests': '["Спорт", "Музыка"]',
            'bio': 'Тестовый пользователь',
            'is_active': True
        }
        
        created_user = adapter.create_user(test_user_data)
        if created_user:
            print("✅ Тестовый пользователь создан успешно!")
            print(f"   ID: {created_user.get('id')}")
            print(f"   Telegram ID: {created_user.get('telegram_id')}")
            
            # Тестируем получение пользователя
            retrieved_user = adapter.get_user_by_telegram_id(999999999)
            if retrieved_user:
                print("✅ Получение пользователя работает!")
            
            # Тестируем обновление пользователя
            update_success = adapter.update_user(999999999, {'bio': 'Обновленный тестовый пользователь'})
            if update_success:
                print("✅ Обновление пользователя работает!")
            
            # Удаляем тестового пользователя
            adapter.supabase.table('users').delete().eq('telegram_id', 999999999).execute()
            print("✅ Тестовый пользователь удален")
        else:
            print("❌ Ошибка при создании тестового пользователя")
        
        # Тестируем поиск пользователей
        print("\n🔍 Тестирование поиска пользователей...")
        search_settings = {
            'gender_preference': 'Все',
            'min_age': 18,
            'max_age': 100,
            'min_height': 140,
            'max_height': 220,
            'min_weight': 40,
            'max_weight': 200
        }
        
        suitable_users = adapter.find_suitable_users(1, search_settings)
        print(f"✅ Поиск пользователей работает! Найдено: {len(suitable_users)}")
        
        print("\n🎉 Все тесты Supabase API прошли успешно!")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании Supabase API: {e}")
        return False

if __name__ == "__main__":
    success = test_supabase_api()
    if success:
        print("\n✅ Supabase API готов к работе!")
    else:
        print("\n❌ Supabase API не работает!")
        sys.exit(1) 