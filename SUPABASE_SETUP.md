# 🚀 Настройка Supabase для бота знакомств

## 📋 Что такое Supabase?

Supabase - это open-source альтернатива Firebase, которая предоставляет:
- **PostgreSQL база данных** (полнофункциональная)
- **Автоматические API** для работы с данными
- **Аутентификация** пользователей
- **Real-time подписки** на изменения данных
- **Хранилище файлов**
- **Edge Functions** (серверные функции)

## 🔧 Пошаговая настройка

### 1. Создание проекта в Supabase

1. Перейдите на [supabase.com](https://supabase.com)
2. Нажмите "Start your project"
3. Войдите через GitHub или создайте аккаунт
4. Создайте новый проект:
   - **Name**: `dating-bot` (или любое другое)
   - **Database Password**: придумайте надежный пароль
   - **Region**: выберите ближайший к вам регион

### 2. Получение данных для подключения

После создания проекта:

1. Перейдите в **Settings** → **Database**
2. Найдите секцию **Connection string**
3. Скопируйте **URI** (он выглядит примерно так):
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres
   ```

4. Перейдите в **Settings** → **API**
5. Скопируйте:
   - **Project URL** (например: `https://your-project.supabase.co`)
   - **anon public** ключ

### 3. Настройка переменных окружения

Создайте файл `.env` в корне проекта:

```bash
# Токен бота Telegram
BOT_TOKEN=8256818214:AAFwnmIc-pKeN8IgpkrW15B6TpUDVdS4ZKI

# Supabase настройки
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-anon-key
SUPABASE_DB_URL=postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres

# Для переключения на Supabase PostgreSQL
DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres
```

### 4. Создание таблиц в Supabase

#### Вариант 1: Автоматическое создание (рекомендуется)

Просто запустите бота - таблицы создадутся автоматически:

```bash
python main.py
```

#### Вариант 2: Ручное создание через SQL Editor

1. Перейдите в **SQL Editor** в панели Supabase
2. Выполните SQL-скрипт:

```sql
-- Создание таблицы пользователей
CREATE TABLE users (
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

-- Создание таблицы настроек поиска
CREATE TABLE search_settings (
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

-- Создание таблицы запросов на доступ
CREATE TABLE access_requests (
    id SERIAL PRIMARY KEY,
    from_user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    to_user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Создание таблицы разрешенных контактов
CREATE TABLE allowed_contacts (
    id SERIAL PRIMARY KEY,
    user1_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    user2_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user1_id, user2_id)
);

-- Создание индексов для оптимизации
CREATE INDEX idx_users_telegram_id ON users(telegram_id);
CREATE INDEX idx_users_gender ON users(gender);
CREATE INDEX idx_users_age ON users(age);
CREATE INDEX idx_users_active ON users(is_active);
CREATE INDEX idx_access_requests_status ON access_requests(status);
CREATE INDEX idx_access_requests_from_user ON access_requests(from_user_id);
CREATE INDEX idx_access_requests_to_user ON access_requests(to_user_id);
```

### 5. Миграция данных из SQLite

Если у вас уже есть данные в SQLite, выполните миграцию:

```bash
# Установите переменную DATABASE_URL для Supabase
export DATABASE_URL="postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres"

# Запустите миграцию
python scripts/migrate_to_supabase.py
```

### 6. Тестирование подключения

Запустите бота для проверки:

```bash
python main.py
```

Вы должны увидеть:
```
✅ Подключение к базе данных успешно!
База данных инициализирована
Бот запущен и готов к работе!
```

## 🔒 Настройка безопасности

### Row Level Security (RLS)

Для дополнительной безопасности включите RLS в Supabase:

1. Перейдите в **Authentication** → **Policies**
2. Включите RLS для всех таблиц
3. Создайте политики доступа

### Пример политики для таблицы users:

```sql
-- Пользователи могут видеть только активных пользователей
CREATE POLICY "Users can view active users" ON users
    FOR SELECT USING (is_active = true);

-- Пользователи могут обновлять только свой профиль
CREATE POLICY "Users can update own profile" ON users
    FOR UPDATE USING (telegram_id = auth.jwt() ->> 'telegram_id');
```

## 📊 Мониторинг и аналитика

### Supabase Dashboard

В панели Supabase вы можете:
- **Database**: просматривать данные в реальном времени
- **Logs**: отслеживать запросы и ошибки
- **Analytics**: анализировать использование
- **API**: тестировать API endpoints

### Полезные SQL запросы

```sql
-- Статистика пользователей
SELECT 
    gender,
    COUNT(*) as count,
    AVG(age) as avg_age
FROM users 
WHERE is_active = true 
GROUP BY gender;

-- Статистика запросов
SELECT 
    status,
    COUNT(*) as count
FROM access_requests 
GROUP BY status;

-- Популярные интересы
SELECT 
    interests,
    COUNT(*) as count
FROM users 
WHERE interests IS NOT NULL 
GROUP BY interests 
ORDER BY count DESC;
```

## 🚀 Преимущества Supabase

1. **Масштабируемость**: PostgreSQL может обрабатывать миллионы записей
2. **Надежность**: автоматические бэкапы и восстановление
3. **Безопасность**: встроенная аутентификация и авторизация
4. **Real-time**: подписки на изменения данных в реальном времени
5. **API**: автоматическая генерация REST API
6. **Мониторинг**: встроенные инструменты аналитики

## 🔧 Устранение неполадок

### Ошибка подключения

```
❌ Ошибка подключения к базе данных: connection failed
```

**Решение:**
1. Проверьте правильность DATABASE_URL
2. Убедитесь, что пароль указан верно
3. Проверьте, что проект не приостановлен

### Ошибка создания таблиц

```
❌ Ошибка при создании таблиц: permission denied
```

**Решение:**
1. Проверьте права доступа в Supabase
2. Убедитесь, что используете правильный ключ API

### Медленные запросы

**Решение:**
1. Создайте индексы для часто используемых полей
2. Оптимизируйте SQL запросы
3. Используйте кэширование

## 📞 Поддержка

- **Supabase Docs**: [supabase.com/docs](https://supabase.com/docs)
- **Supabase Discord**: [discord.supabase.com](https://discord.supabase.com)
- **GitHub Issues**: [github.com/supabase/supabase](https://github.com/supabase/supabase) 