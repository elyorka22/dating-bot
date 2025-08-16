#!/usr/bin/env python3
"""
Скрипт для деплоя бота на Beget
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Проверка версии Python"""
    if sys.version_info < (3, 8):
        print("❌ Требуется Python 3.8+")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}")
    return True

def create_virtual_environment():
    """Создание виртуального окружения"""
    if not Path("venv").exists():
        print("🔧 Создание виртуального окружения...")
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✅ Виртуальное окружение создано")
    else:
        print("✅ Виртуальное окружение уже существует")

def install_dependencies():
    """Установка зависимостей"""
    print("📦 Установка зависимостей...")
    
    # Активируем виртуальное окружение
    if os.name == 'nt':  # Windows
        pip_path = "venv\\Scripts\\pip"
    else:  # Linux/Mac
        pip_path = "venv/bin/pip"
    
    subprocess.run([pip_path, "install", "-r", "requirements.txt"], check=True)
    print("✅ Зависимости установлены")

def create_beget_config():
    """Создание конфигурации для Beget"""
    print("⚙️ Создание конфигурации для Beget...")
    
    # Создаем .htaccess для Python
    htaccess_content = """
RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-f
RewriteRule ^(.*)$ main.py/$1 [QSA,L]

# Запуск Python скрипта
AddHandler cgi-script .py
Options +ExecCGI
"""
    
    with open(".htaccess", "w", encoding="utf-8") as f:
        f.write(htaccess_content)
    
    # Создаем конфигурацию для Beget
    beget_config = """
# Конфигурация для Beget
# Разместите файлы в папке public_html или www

# Структура папок:
# public_html/
# ├── main.py
# ├── config.py
# ├── requirements.txt
# ├── .htaccess
# ├── .env
# └── остальные файлы

# В .env укажите:
# BOT_TOKEN=ваш_токен_бота
# DATABASE_URL=sqlite:///dating_bot.db
# SUPABASE_URL=ваш_supabase_url
# SUPABASE_KEY=ваш_supabase_key
"""
    
    with open("BEGET_CONFIG.md", "w", encoding="utf-8") as f:
        f.write(beget_config)
    
    print("✅ Конфигурация создана")

def create_startup_script():
    """Создание скрипта запуска"""
    print("🚀 Создание скрипта запуска...")
    
    startup_script = """#!/usr/bin/env python3
# Скрипт запуска для Beget
import os
import sys

# Добавляем путь к проекту
project_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_path)

# Импортируем и запускаем бота
from main import main
import asyncio

if __name__ == "__main__":
    asyncio.run(main())
"""
    
    with open("start_bot.py", "w", encoding="utf-8") as f:
        f.write(startup_script)
    
    # Делаем скрипт исполняемым
    os.chmod("start_bot.py", 0o755)
    
    print("✅ Скрипт запуска создан")

def create_cron_job():
    """Создание cron задачи"""
    print("⏰ Создание cron задачи...")
    
    cron_content = """# Cron задача для запуска бота на Beget
# Добавьте эту строку в cron через панель управления Beget:

# Запуск бота каждые 5 минут (проверка и перезапуск)
*/5 * * * * cd /home/username/public_html && python3 start_bot.py

# Или запуск при загрузке системы
@reboot cd /home/username/public_html && python3 start_bot.py

# Замените username на ваше имя пользователя
"""
    
    with open("cron_setup.txt", "w", encoding="utf-8") as f:
        f.write(cron_content)
    
    print("✅ Cron задача создана")

def create_deployment_guide():
    """Создание руководства по деплою"""
    print("📚 Создание руководства по деплою...")
    
    guide = """# 🚀 Руководство по деплою на Beget

## 📋 Подготовка

1. **Зарегистрируйтесь на Beget**
   - Перейдите на beget.com
   - Выберите тарифный план с поддержкой Python
   - Получите доступ к панели управления

2. **Подготовьте файлы**
   - Все файлы проекта должны быть в папке public_html
   - Убедитесь, что .env настроен правильно

## 🔧 Настройка на Beget

### 1. Загрузка файлов
- Загрузите все файлы проекта в папку public_html
- Убедитесь, что права доступа установлены правильно (644 для файлов, 755 для папок)

### 2. Настройка Python
- В панели управления Beget перейдите в раздел "Python"
- Создайте Python приложение
- Укажите путь к main.py
- Установите версию Python 3.8+

### 3. Настройка базы данных
- Создайте MySQL базу данных в панели управления
- Или используйте SQLite (файл dating_bot.db)
- Обновите DATABASE_URL в .env

### 4. Настройка cron
- Перейдите в раздел "Cron" в панели управления
- Добавьте задачу из файла cron_setup.txt
- Убедитесь, что путь указан правильно

## 🚀 Запуск

### Вариант 1: Через Python приложение
1. Настройте Python приложение в панели управления
2. Укажите путь к main.py
3. Запустите приложение

### Вариант 2: Через cron
1. Добавьте cron задачу
2. Бот будет автоматически запускаться и перезапускаться

### Вариант 3: Вручную
```bash
cd /home/username/public_html
python3 start_bot.py
```

## 📊 Мониторинг

### Логи
- Логи сохраняются в папке logs/
- Проверяйте логи через файловый менеджер Beget

### Статус
- Проверяйте статус бота через Telegram
- Отправьте команду /start боту

## 🔧 Troubleshooting

### Бот не запускается
1. Проверьте права доступа к файлам
2. Проверьте настройки Python в панели управления
3. Проверьте логи в папке logs/

### Ошибки базы данных
1. Проверьте настройки DATABASE_URL в .env
2. Убедитесь, что база данных создана
3. Проверьте права доступа к базе данных

### Проблемы с cron
1. Проверьте путь в cron задаче
2. Убедитесь, что Python доступен в cron
3. Проверьте логи cron в панели управления

## 📞 Поддержка

- Техподдержка Beget: support@beget.com
- Документация: help.beget.com
- Логи проекта: logs/dating_bot_errors_YYYYMMDD.log
"""
    
    with open("BEGET_DEPLOYMENT_GUIDE.md", "w", encoding="utf-8") as f:
        f.write(guide)
    
    print("✅ Руководство по деплою создано")

def main():
    """Главная функция подготовки к деплою"""
    print("🚀 Подготовка к деплою на Beget\n")
    
    try:
        # Проверяем версию Python
        if not check_python_version():
            return False
        
        # Создаем виртуальное окружение
        create_virtual_environment()
        
        # Устанавливаем зависимости
        install_dependencies()
        
        # Создаем конфигурацию
        create_beget_config()
        
        # Создаем скрипт запуска
        create_startup_script()
        
        # Создаем cron задачу
        create_cron_job()
        
        # Создаем руководство
        create_deployment_guide()
        
        print("\n🎉 Подготовка к деплою завершена!")
        print("\n📋 Следующие шаги:")
        print("1. Зарегистрируйтесь на beget.com")
        print("2. Выберите тарифный план с поддержкой Python")
        print("3. Загрузите файлы в папку public_html")
        print("4. Настройте Python приложение в панели управления")
        print("5. Настройте cron задачу")
        print("6. Запустите бота")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при подготовке: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1) 