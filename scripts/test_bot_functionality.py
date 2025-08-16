#!/usr/bin/env python3
"""
Быстрый тест функциональности бота
"""

import os
import sys

# Добавляем корневую директорию в путь
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_database():
    """Тест базы данных"""
    print("🗄️ Тестирование базы данных...")
    
    try:
        from database.database import check_database_connection, create_tables
        
        if check_database_connection():
            print("✅ Подключение к базе данных успешно")
            create_tables()
            print("✅ Таблицы созданы/обновлены")
            return True
        else:
            print("❌ Ошибка подключения к базе данных")
            return False
    except Exception as e:
        print(f"❌ Ошибка тестирования БД: {e}")
        return False

def test_translations():
    """Тест переводов"""
    print("\n🌍 Тестирование переводов...")
    
    try:
        from locales.translations import get_text, is_supported_language
        
        # Проверяем поддержку языков
        if is_supported_language('ru') and is_supported_language('uz'):
            print("✅ Поддержка языков работает")
        else:
            print("❌ Ошибка поддержки языков")
            return False
        
        # Тестируем переводы
        ru_text = get_text('welcome', 'ru')
        uz_text = get_text('welcome', 'uz')
        
        if ru_text and uz_text and ru_text != uz_text:
            print("✅ Переводы работают корректно")
            print(f"   RU: {ru_text}")
            print(f"   UZ: {uz_text}")
            return True
        else:
            print("❌ Ошибка переводов")
            return False
    except Exception as e:
        print(f"❌ Ошибка тестирования переводов: {e}")
        return False

def test_keyboards():
    """Тест клавиатур"""
    print("\n⌨️ Тестирование клавиатур...")
    
    try:
        # Тестируем основные клавиатуры
        from keyboards.inline import get_main_menu_keyboard
        from keyboards.settings import get_settings_menu_keyboard
        from keyboards.profile import get_profile_edit_keyboard
        from keyboards.language import get_language_keyboard
        
        main_menu_ru = get_main_menu_keyboard('ru')
        main_menu_uz = get_main_menu_keyboard('uz')
        
        settings_menu_ru = get_settings_menu_keyboard('ru')
        settings_menu_uz = get_settings_menu_keyboard('uz')
        
        profile_edit_ru = get_profile_edit_keyboard('ru')
        profile_edit_uz = get_profile_edit_keyboard('uz')
        
        language_kb = get_language_keyboard()
        
        print("✅ Все клавиатуры создаются успешно")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка создания клавиатур: {e}")
        return False

def test_config():
    """Тест конфигурации"""
    print("\n⚙️ Тестирование конфигурации...")
    
    try:
        from config import BOT_TOKEN, DATABASE_URL, SUPABASE_URL, SUPABASE_KEY
        
        if BOT_TOKEN and len(BOT_TOKEN) > 10:
            print("✅ Токен бота настроен")
        else:
            print("❌ Токен бота не настроен")
            return False
        
        if DATABASE_URL:
            print("✅ URL базы данных настроен")
        else:
            print("❌ URL базы данных не настроен")
            return False
        
        if SUPABASE_URL and SUPABASE_KEY:
            print("✅ Supabase настройки готовы")
        else:
            print("⚠️ Supabase настройки не полные")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка конфигурации: {e}")
        return False

def main():
    """Главная функция тестирования"""
    print("🚀 Быстрый тест функциональности бота\n")
    
    tests = [
        ("База данных", test_database),
        ("Переводы", test_translations),
        ("Клавиатуры", test_keyboards),
        ("Конфигурация", test_config)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ Тест '{test_name}' провален")
        except Exception as e:
            print(f"❌ Тест '{test_name}' вызвал ошибку: {e}")
    
    print(f"\n📊 Результаты: {passed}/{total} тестов пройдено")
    
    if passed == total:
        print("🎉 Все тесты пройдены! Бот готов к базовому тестированию.")
        return True
    else:
        print("⚠️ Некоторые тесты провалены. Нужно исправить ошибки.")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1) 