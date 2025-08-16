# 🐧 Настройка Ubuntu VPS на Beget для Telegram бота

## 🎯 Выбор тарифного плана

### Рекомендуемые тарифы Beget VPS:
- **VPS-1** (1 CPU, 1GB RAM, 20GB SSD) - от 200₽/месяц
- **VPS-2** (2 CPU, 2GB RAM, 40GB SSD) - от 400₽/месяц
- **VPS-3** (4 CPU, 4GB RAM, 80GB SSD) - от 800₽/месяц

### Для Telegram бота достаточно VPS-1!

## 🚀 Пошаговая настройка

### 1. **Создание VPS на Beget**
1. Войдите в панель управления Beget
2. Перейдите в раздел "VPS"
3. Нажмите "Создать VPS"
4. Выберите:
   - **ОС**: Ubuntu 22.04 LTS
   - **Тариф**: VPS-1 (для начала)
   - **Локация**: Москва (быстрее)
   - **SSH ключ**: Создайте новый

### 2. **Подключение к серверу**
```bash
# Получите IP адрес и пароль от VPS
ssh root@YOUR_VPS_IP

# Или используйте SSH ключ
ssh -i ~/.ssh/beget_key root@YOUR_VPS_IP
```

### 3. **Обновление системы**
```bash
# Обновляем пакеты
apt update && apt upgrade -y

# Устанавливаем необходимые пакеты
apt install -y python3 python3-pip python3-venv git curl wget htop
```

### 4. **Создание пользователя для бота**
```bash
# Создаем пользователя
adduser botuser
usermod -aG sudo botuser

# Переключаемся на пользователя
su - botuser
```

### 5. **Установка Python зависимостей**
```bash
# Создаем папку для проекта
mkdir -p /home/botuser/dating_bot
cd /home/botuser/dating_bot

# Создаем виртуальное окружение
python3 -m venv venv
source venv/bin/activate

# Устанавливаем зависимости
pip install --upgrade pip
pip install -r requirements.txt
```

### 6. **Загрузка кода бота**
```bash
# Клонируем репозиторий (если используете Git)
git clone https://github.com/your-repo/dating-bot.git .

# Или загружаем файлы через SCP
scp -r /path/to/local/files/* botuser@YOUR_VPS_IP:/home/botuser/dating_bot/
```

### 7. **Настройка переменных окружения**
```bash
# Создаем .env файл
nano .env

# Добавляем настройки:
BOT_TOKEN=8256818214:AAFwnmIc-pKeN8IgpkrW15B6TpUDVdS4ZKI
DATABASE_URL=sqlite:///dating_bot.db
SUPABASE_URL=https://jcouuxyzslspubviwfnz.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Impjb3V1eHl6c2xzcHVidml3ZnN6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTUyOTMwNTYsImV4cCI6MjA3MDg2OTA1Nn0.mPtyUI9wzj8fDYdtYceDn7zQJmH_zsMHbpAQxXXiJuU
LOG_LEVEL=INFO
LOG_FILE=logs/dating_bot.log
```

### 8. **Создание systemd сервиса**
```bash
# Создаем файл сервиса
sudo nano /etc/systemd/system/dating-bot.service
```

**Содержимое файла:**
```ini
[Unit]
Description=Dating Bot Telegram
After=network.target

[Service]
Type=simple
User=botuser
WorkingDirectory=/home/botuser/dating_bot
Environment=PATH=/home/botuser/dating_bot/venv/bin
ExecStart=/home/botuser/dating_bot/venv/bin/python main.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

### 9. **Запуск сервиса**
```bash
# Перезагружаем systemd
sudo systemctl daemon-reload

# Включаем автозапуск
sudo systemctl enable dating-bot

# Запускаем сервис
sudo systemctl start dating-bot

# Проверяем статус
sudo systemctl status dating-bot
```

### 10. **Настройка firewall**
```bash
# Устанавливаем ufw
sudo apt install ufw

# Разрешаем SSH
sudo ufw allow ssh

# Разрешаем HTTP/HTTPS (если понадобится)
sudo ufw allow 80
sudo ufw allow 443

# Включаем firewall
sudo ufw enable
```

## 🔧 Управление ботом

### Просмотр логов
```bash
# Логи systemd
sudo journalctl -u dating-bot -f

# Логи приложения
tail -f /home/botuser/dating_bot/logs/dating_bot.log
```

### Управление сервисом
```bash
# Остановить бота
sudo systemctl stop dating-bot

# Перезапустить бота
sudo systemctl restart dating-bot

# Проверить статус
sudo systemctl status dating-bot
```

### Обновление бота
```bash
# Останавливаем сервис
sudo systemctl stop dating-bot

# Обновляем код
cd /home/botuser/dating_bot
git pull  # или загружаем новые файлы

# Обновляем зависимости
source venv/bin/activate
pip install -r requirements.txt

# Запускаем сервис
sudo systemctl start dating-bot
```

## 📊 Мониторинг

### Установка мониторинга
```bash
# Устанавливаем htop для мониторинга ресурсов
sudo apt install htop

# Запускаем мониторинг
htop
```

### Проверка ресурсов
```bash
# Использование CPU и памяти
top

# Использование диска
df -h

# Использование памяти
free -h
```

## 🔒 Безопасность

### Обновление системы
```bash
# Регулярно обновляйте систему
sudo apt update && sudo apt upgrade -y
```

### Резервное копирование
```bash
# Создаем скрипт для бэкапа
nano /home/botuser/backup.sh
```

**Содержимое backup.sh:**
```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/home/botuser/backups"
mkdir -p $BACKUP_DIR

# Бэкап базы данных
cp /home/botuser/dating_bot/dating_bot.db $BACKUP_DIR/dating_bot_$DATE.db

# Бэкап логов
tar -czf $BACKUP_DIR/logs_$DATE.tar.gz /home/botuser/dating_bot/logs/

# Удаляем старые бэкапы (старше 7 дней)
find $BACKUP_DIR -name "*.db" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
```

## 🆘 Troubleshooting

### Бот не запускается
```bash
# Проверяем логи
sudo journalctl -u dating-bot -n 50

# Проверяем права доступа
ls -la /home/botuser/dating_bot/

# Проверяем Python
python3 --version
```

### Проблемы с базой данных
```bash
# Проверяем файл базы данных
ls -la /home/botuser/dating_bot/dating_bot.db

# Проверяем права доступа
sudo chown botuser:botuser /home/botuser/dating_bot/dating_bot.db
```

### Высокое потребление ресурсов
```bash
# Проверяем процессы
ps aux | grep python

# Проверяем использование памяти
free -h

# Перезапускаем сервис
sudo systemctl restart dating-bot
```

## 📞 Поддержка

- **Beget VPS поддержка**: support@beget.com
- **Ubuntu документация**: ubuntu.com/server/docs
- **Systemd документация**: systemd.io

## 🎯 Готово!

После выполнения всех шагов ваш бот будет работать на Ubuntu VPS!

### Преимущества этого подхода:
- ✅ Полный контроль над сервером
- ✅ Лучшая производительность
- ✅ Возможность масштабирования
- ✅ Профессиональная настройка
- ✅ Автоматический перезапуск
- ✅ Мониторинг и логирование 