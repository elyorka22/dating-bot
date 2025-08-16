# 🚀 Руководство по развертыванию

## 📋 Требования

### Системные требования
- Python 3.8+
- PostgreSQL 12+ (или Supabase)
- 512MB RAM минимум
- 1GB свободного места

### Зависимости
- aiogram 3.21.0
- SQLAlchemy 2.0.25+
- psycopg2-binary 2.9.10+
- supabase 2.18.1+

## 🔧 Установка

### 1. Клонирование репозитория
```bash
git clone <repository-url>
cd dating-bot
```

### 2. Создание виртуального окружения
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows
```

### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 4. Настройка переменных окружения
Создайте файл `.env` на основе `env_example.txt`:
```bash
cp env_example.txt .env
```

Заполните необходимые переменные:
```env
# Telegram Bot
BOT_TOKEN=your_bot_token_here

# Database
DATABASE_URL=sqlite:///dating_bot.db  # Для разработки
# DATABASE_URL=postgresql://user:pass@host:port/db  # Для продакшена

# Supabase (для продакшена)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_anon_key
SUPABASE_DB_URL=postgresql://postgres:password@db.project.supabase.co:5432/postgres
```

## 🗄️ Настройка базы данных

### Вариант 1: Supabase (рекомендуется для продакшена)

1. Создайте проект на [supabase.com](https://supabase.com)
2. Получите URL и ключи из настроек проекта
3. Обновите переменные окружения
4. Запустите миграцию:
```bash
python scripts/create_tables_supabase.py
```

### Вариант 2: Локальный PostgreSQL

1. Установите PostgreSQL
2. Создайте базу данных:
```sql
CREATE DATABASE dating_bot;
CREATE USER dating_bot_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE dating_bot TO dating_bot_user;
```

3. Обновите `DATABASE_URL` в `.env`

## 🚀 Запуск

### Режим разработки
```bash
python main.py
```

### Продакшен режим

#### Вариант 1: Systemd (Linux)
Создайте файл `/etc/systemd/system/dating-bot.service`:
```ini
[Unit]
Description=Dating Bot
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/dating-bot
Environment=PATH=/path/to/dating-bot/venv/bin
ExecStart=/path/to/dating-bot/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Запустите сервис:
```bash
sudo systemctl daemon-reload
sudo systemctl enable dating-bot
sudo systemctl start dating-bot
```

#### Вариант 2: Docker
Создайте `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

Создайте `docker-compose.yml`:
```yaml
version: '3.8'
services:
  dating-bot:
    build: .
    environment:
      - BOT_TOKEN=${BOT_TOKEN}
      - DATABASE_URL=${DATABASE_URL}
      - SUPABASE_URL=${SUPABASE_URL}
      - SUPABASE_KEY=${SUPABASE_KEY}
    restart: unless-stopped
    volumes:
      - ./logs:/app/logs
```

Запустите:
```bash
docker-compose up -d
```

## 📊 Мониторинг

### Логи
Логи сохраняются в директории `logs/`:
- `dating_bot_YYYYMMDD.log` - все логи
- `dating_bot_errors_YYYYMMDD.log` - только ошибки

### Проверка статуса
```bash
# Systemd
sudo systemctl status dating-bot

# Docker
docker-compose ps
docker-compose logs -f dating-bot
```

### Тестирование
```bash
# Тест функциональности
python scripts/test_bot_functionality.py

# Тест безопасности
python scripts/test_security.py
```

## 🔒 Безопасность

### Настройки безопасности
- Валидация всех входных данных
- Защита от спама (rate limiting)
- Санитизация текста
- Логирование всех действий

### Рекомендации
1. Используйте HTTPS для всех соединений
2. Регулярно обновляйте зависимости
3. Мониторьте логи на подозрительную активность
4. Настройте резервное копирование базы данных

## 📈 Масштабирование

### Горизонтальное масштабирование
1. Используйте Redis для кэширования
2. Настройте load balancer
3. Разделите базу данных на read/write реплики

### Вертикальное масштабирование
1. Увеличьте RAM и CPU
2. Оптимизируйте запросы к базе данных
3. Настройте connection pooling

## 🔄 Обновления

### Процедура обновления
1. Остановите бота
2. Создайте резервную копию базы данных
3. Обновите код
4. Запустите миграции (если есть)
5. Запустите бота
6. Проверьте работоспособность

### Автоматические обновления
Настройте CI/CD pipeline для автоматического развертывания.

## 🆘 Troubleshooting

### Частые проблемы

#### Бот не запускается
1. Проверьте токен бота
2. Проверьте подключение к базе данных
3. Проверьте логи в `logs/`

#### Ошибки базы данных
1. Проверьте подключение к PostgreSQL
2. Проверьте права доступа пользователя
3. Запустите миграции

#### Высокая нагрузка
1. Проверьте rate limiting
2. Оптимизируйте запросы к БД
3. Увеличьте ресурсы сервера

### Контакты для поддержки
- Логи: `logs/dating_bot_errors_YYYYMMDD.log`
- Конфигурация: `config.py`, `.env`
- Статус: `sudo systemctl status dating-bot`

## 📝 Чек-лист развертывания

- [ ] Установлены все зависимости
- [ ] Настроены переменные окружения
- [ ] База данных создана и настроена
- [ ] Запущены миграции
- [ ] Протестирована функциональность
- [ ] Протестирована безопасность
- [ ] Настроен мониторинг
- [ ] Настроено резервное копирование
- [ ] Документированы процедуры обновления 