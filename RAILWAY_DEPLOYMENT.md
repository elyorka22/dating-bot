# 🚀 Деплой бота знакомств в Railway

## 📋 Подготовка к деплою

### 1️⃣ Создайте аккаунт на Railway
- Перейдите на [railway.app](https://railway.app)
- Зарегистрируйтесь через GitHub
- Подтвердите email

### 2️⃣ Подготовьте репозиторий
```bash
# Инициализируйте Git репозиторий (если еще не сделано)
git init
git add .
git commit -m "Подготовка к деплою в Railway"

# Создайте репозиторий на GitHub
# Загрузите код на GitHub
```

### 3️⃣ Создайте проект в Railway
1. Нажмите "New Project"
2. Выберите "Deploy from GitHub repo"
3. Выберите ваш репозиторий
4. Railway автоматически определит Python проект

## ⚙️ Настройка переменных окружения

### В Railway Dashboard:
1. Перейдите в ваш проект
2. Нажмите на вкладку "Variables"
3. Добавьте следующие переменные:

```
BOT_TOKEN=8256818214:AAFwnmIc-pKeN8IgpkrW15B6TpUDVdS4ZKI
SUPABASE_URL=https://jcouuxyzslspubviwfnz.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Impjb3V1eHl6c2xzcHVidml3Zm56Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTUyOTMwNTYsImV4cCI6MjA3MDg2OTA1Nn0.mPtyUI9wzj8fDYdtYceDn7zQJmH_zsMHbpAQxXXiJuU
MAX_REQUESTS_PER_DAY=20
LOG_LEVEL=INFO
ENVIRONMENT=production
```

### Опциональные переменные:
```
MIN_AGE=18
MAX_AGE=100
MIN_HEIGHT=140
MAX_HEIGHT=220
MIN_WEIGHT=40
MAX_WEIGHT=200
BOT_POLLING_TIMEOUT=30
BOT_POLLING_LIMIT=100
SKIP_UPDATES=true
RATE_LIMIT_ENABLED=true
SPAM_PROTECTION_ENABLED=true
```

## 🗄️ Настройка базы данных

### Вариант 1: PostgreSQL от Railway (рекомендуется)
1. В Railway Dashboard нажмите "New"
2. Выберите "Database" → "PostgreSQL"
3. Railway автоматически создаст DATABASE_URL
4. Переменная DATABASE_URL будет доступна автоматически

### Вариант 2: Использовать Supabase
- Оставьте настройки Supabase как есть
- Бот будет использовать Supabase PostgreSQL

## 🚀 Деплой

### Автоматический деплой:
1. Railway автоматически деплоит при push в GitHub
2. Следите за логами в Railway Dashboard
3. Дождитесь успешного деплоя

### Ручной деплой:
1. В Railway Dashboard нажмите "Deploy"
2. Выберите ветку для деплоя
3. Дождитесь завершения

## ✅ Проверка работы

### 1️⃣ Проверьте логи:
- В Railway Dashboard перейдите в "Deployments"
- Нажмите на последний деплой
- Проверьте логи на ошибки

### 2️⃣ Протестируйте бота:
- Откройте Telegram
- Найдите вашего бота
- Отправьте `/start`
- Проверьте все функции

## 🔧 Устранение проблем

### Проблема: Бот не отвечает
**Решение:**
1. Проверьте переменную BOT_TOKEN
2. Убедитесь, что бот не заблокирован
3. Проверьте логи в Railway

### Проблема: Ошибки базы данных
**Решение:**
1. Проверьте DATABASE_URL
2. Убедитесь, что PostgreSQL запущен
3. Проверьте права доступа

### Проблема: Медленная работа
**Решение:**
1. Увеличьте ресурсы в Railway
2. Проверьте настройки производительности
3. Оптимизируйте запросы к БД

## 📊 Мониторинг

### Railway Dashboard:
- **Logs**: Просмотр логов в реальном времени
- **Metrics**: Мониторинг ресурсов
- **Deployments**: История деплоев

### Telegram Bot API:
- Проверьте статус бота через @BotFather
- Мониторьте количество пользователей

## 💰 Стоимость

### Railway Pricing:
- **Free Tier**: $5 кредитов в месяц
- **Pro**: $20/месяц
- **Team**: $20/пользователь/месяц

### Рекомендации:
- Начните с Free Tier
- Мониторьте использование ресурсов
- При необходимости переходите на Pro

## 🔄 Обновления

### Автоматические обновления:
1. Внесите изменения в код
2. Загрузите на GitHub
3. Railway автоматически деплоит

### Откат к предыдущей версии:
1. В Railway Dashboard перейдите в "Deployments"
2. Найдите нужную версию
3. Нажмите "Redeploy"

## 🎉 Готово!

Ваш бот знакомств успешно развернут в Railway!

**Преимущества Railway:**
- ✅ Автоматические деплои
- ✅ Встроенная база данных
- ✅ Мониторинг и логи
- ✅ Масштабируемость
- ✅ Простота использования 