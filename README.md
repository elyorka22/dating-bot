# Telegram Dating Bot

Бот знакомств для Telegram с поддержкой русского и узбекского языков.

## Функции

- 👤 Создание профиля пользователя (пол, возраст, рост, вес, семейное положение, интересы)
- 🔍 Поиск людей по критериям
- 📨 Система запросов на доступ к личным сообщениям
- 🌍 Поддержка русского и узбекского языков
- 💾 База данных PostgreSQL/SQLite

## Технологии

- Python 3.11
- aiogram 3.x
- SQLAlchemy
- PostgreSQL/SQLite
- Railway (деплой)

## Структура проекта

```
├── main.py              # Основной файл бота
├── config.py            # Конфигурация
├── requirements.txt     # Зависимости
├── Procfile            # Конфигурация Railway
├── railway.json        # Настройки Railway
├── runtime.txt         # Версия Python
├── database/           # Модели и работа с БД
│   ├── models.py
│   ├── database.py
│   └── __init__.py
├── handlers/           # Обработчики
│   ├── user.py
│   ├── requests.py
│   └── __init__.py
├── keyboards/          # Клавиатуры
│   ├── base.py
│   └── __init__.py
└── locales/           # Переводы
    ├── translations.py
    └── __init__.py
```

## Установка и запуск

1. Клонируйте репозиторий
2. Установите зависимости: `pip install -r requirements.txt`
3. Создайте файл `.env` с переменными окружения
4. Запустите бота: `python main.py`

## Переменные окружения

- `BOT_TOKEN` - токен Telegram бота
- `DATABASE_URL` - URL базы данных (автоматически устанавливается Railway)

## Деплой на Railway

1. Подключите GitHub репозиторий к Railway
2. Установите переменную окружения `BOT_TOKEN`
3. Railway автоматически установит `DATABASE_URL`
4. Деплой запустится автоматически

## Команды бота

- `/start` - Начать работу с ботом 