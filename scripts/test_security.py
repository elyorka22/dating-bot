#!/usr/bin/env python3
"""
Тест системы безопасности (валидация + защита от спама)
"""

import os
import sys
import time

# Добавляем корневую директорию в путь
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_validators():
    """Тест валидаторов"""
    print("🔒 Тестирование валидаторов...")
    
    try:
        from utils.validators import (
            validate_age, validate_height, validate_weight, validate_gender,
            validate_marital_status, validate_interests, validate_bio, sanitize_text
        )
        
        # Тест валидации возраста
        assert validate_age("25")[0] == True, "Валидный возраст должен проходить"
        assert validate_age("150")[0] == False, "Невалидный возраст должен отклоняться"
        assert validate_age("abc")[0] == False, "Нечисловой возраст должен отклоняться"
        
        # Тест валидации роста
        assert validate_height("170")[0] == True, "Валидный рост должен проходить"
        assert validate_height("300")[0] == False, "Невалидный рост должен отклоняться"
        
        # Тест валидации веса
        assert validate_weight("70")[0] == True, "Валидный вес должен проходить"
        assert validate_weight("500")[0] == False, "Невалидный вес должен отклоняться"
        
        # Тест валидации пола
        assert validate_gender("Мужчина")[0] == True, "Валидный пол должен проходить"
        assert validate_gender("Неизвестно")[0] == False, "Невалидный пол должен отклоняться"
        
        # Тест валидации семейного положения
        assert validate_marital_status("Холост/Не замужем")[0] == True, "Валидный статус должен проходить"
        assert validate_marital_status("Неизвестно")[0] == False, "Невалидный статус должен отклоняться"
        
        # Тест валидации интересов
        assert validate_interests(["Спорт", "Музыка"])[0] == True, "Валидные интересы должны проходить"
        assert validate_interests(["Неизвестный интерес"])[0] == False, "Невалидные интересы должны отклоняться"
        
        # Тест валидации описания
        assert validate_bio("Обычное описание")[0] == True, "Валидное описание должно проходить"
        assert validate_bio("a" * 600)[0] == False, "Слишком длинное описание должно отклоняться"
        assert validate_bio("Ссылка: http://example.com")[0] == False, "Описание со ссылкой должно отклоняться"
        
        # Тест санитизации
        assert sanitize_text("  <script>alert('test')</script>  ") == "alert('test')", "HTML теги должны удаляться"
        assert sanitize_text("  много   пробелов  ") == "много пробелов", "Множественные пробелы должны нормализоваться"
        
        print("✅ Все валидаторы работают корректно")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка тестирования валидаторов: {e}")
        return False

def test_rate_limiter():
    """Тест rate limiter"""
    print("\n⏱️ Тестирование rate limiter...")
    
    try:
        from utils.rate_limiter import RateLimiter
        
        limiter = RateLimiter()
        user_id = 12345
        
        # Тест базового лимита
        assert limiter.is_allowed(user_id, 'message') == True, "Первый запрос должен быть разрешен"
        assert limiter.get_remaining_requests(user_id, 'message') == 9, "Должно остаться 9 запросов"
        
        # Тест превышения лимита
        for i in range(10):
            limiter.is_allowed(user_id, 'message')
        
        assert limiter.is_allowed(user_id, 'message') == False, "После превышения лимита запрос должен быть заблокирован"
        assert limiter.get_remaining_requests(user_id, 'message') == 0, "Должно остаться 0 запросов"
        
        # Тест сброса лимитов
        limiter.reset_user_limits(user_id)
        assert limiter.is_allowed(user_id, 'message') == True, "После сброса запрос должен быть разрешен"
        
        print("✅ Rate limiter работает корректно")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка тестирования rate limiter: {e}")
        return False

def test_spam_protection():
    """Тест защиты от спама"""
    print("\n🛡️ Тестирование защиты от спама...")
    
    try:
        from utils.rate_limiter import spam_protection
        
        user_id = 54321
        
        # Тест проверки сообщений
        spam_check = spam_protection.check_message_spam(user_id, "Обычное сообщение")
        assert spam_check['is_spam'] == False, "Обычное сообщение не должно считаться спамом"
        
        spam_check = spam_protection.check_message_spam(user_id, "СООБЩЕНИЕ ВСЕМИ ЗАГЛАВНЫМИ БУКВАМИ")
        assert spam_check['is_spam'] == True, "Сообщение в капсе должно считаться спамом"
        assert spam_check['action'] == 'warn', "Капс должен вызывать предупреждение"
        
        spam_check = spam_protection.check_message_spam(user_id, "Сообщение с ссылкой http://example.com")
        assert spam_check['is_spam'] == True, "Сообщение со ссылкой должно считаться спамом"
        assert spam_check['action'] == 'block', "Ссылки должны блокироваться"
        
        spam_check = spam_protection.check_message_spam(user_id, "Сообщение с повторяющимися символами ааааааа")
        assert spam_check['is_spam'] == True, "Повторяющиеся символы должны считаться спамом"
        
        # Тест проверки действий
        action_check = spam_protection.check_action_spam(user_id, 'search')
        assert action_check['is_spam'] == False, "Первое действие не должно считаться спамом"
        
        # Тест записи ошибок
        spam_protection.record_error(user_id, 'invalid_inputs')
        spam_protection.record_error(user_id, 'repeated_errors')
        
        print("✅ Защита от спама работает корректно")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка тестирования защиты от спама: {e}")
        return False

def test_integration():
    """Интеграционный тест"""
    print("\n🔗 Интеграционный тест...")
    
    try:
        from utils.validators import validate_age, sanitize_text
        from utils.rate_limiter import spam_protection
        
        user_id = 99999
        
        # Тест полного цикла
        # 1. Проверяем rate limiting
        spam_check = spam_protection.check_action_spam(user_id, 'message')
        assert spam_check['is_spam'] == False, "Первый запрос должен быть разрешен"
        
        # 2. Валидируем данные
        is_valid, age_value, error_msg = validate_age("25")
        assert is_valid == True, "Валидный возраст должен проходить"
        assert age_value == 25, "Возраст должен быть правильно извлечен"
        
        # 3. Санитизируем текст
        sanitized = sanitize_text("  <b>текст</b>  ")
        assert sanitized == "текст", "Текст должен быть правильно санитизирован"
        
        print("✅ Интеграционный тест прошел успешно")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка интеграционного теста: {e}")
        return False

def main():
    """Главная функция тестирования"""
    print("🔒 Тест системы безопасности\n")
    
    tests = [
        ("Валидаторы", test_validators),
        ("Rate Limiter", test_rate_limiter),
        ("Защита от спама", test_spam_protection),
        ("Интеграционный тест", test_integration)
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
        print("🎉 Все тесты безопасности пройдены! Система готова к продакшену.")
        return True
    else:
        print("⚠️ Некоторые тесты безопасности провалены. Нужно исправить ошибки.")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1) 