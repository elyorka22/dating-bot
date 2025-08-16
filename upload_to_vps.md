# 📤 Загрузка файлов на Ubuntu VPS

## 🚀 Быстрая загрузка через SCP

### 1. **Подготовка файлов локально**
```bash
# Создайте архив с файлами бота
tar -czf dating_bot.tar.gz \
    main.py \
    config.py \
    requirements.txt \
    database/ \
    handlers/ \
    keyboards/ \
    locales/ \
    services/ \
    utils/ \
    scripts/ \
    .env_beget
```

### 2. **Загрузка на VPS**
```bash
# Загрузите архив на VPS
scp dating_bot.tar.gz botuser@YOUR_VPS_IP:/home/botuser/dating_bot/

# Подключитесь к VPS
ssh botuser@YOUR_VPS_IP

# Распакуйте архив
cd /home/botuser/dating_bot
tar -xzf dating_bot.tar.gz
rm dating_bot.tar.gz
```

## 🔧 Альтернативные способы загрузки

### **Через Git (рекомендуется)**
```bash
# На VPS
cd /home/botuser/dating_bot
git clone https://github.com/your-repo/dating-bot.git .
```

### **Через rsync**
```bash
# Синхронизация папки
rsync -avz --exclude 'venv' --exclude '__pycache__' \
    /path/to/local/dating_bot/ \
    botuser@YOUR_VPS_IP:/home/botuser/dating_bot/
```

### **Через SFTP**
```bash
# Подключение через SFTP
sftp botuser@YOUR_VPS_IP
cd /home/botuser/dating_bot
put -r /path/to/local/files/*
```

## ⚙️ Настройка после загрузки

### 1. **Создание виртуального окружения**
```bash
cd /home/botuser/dating_bot
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 2. **Настройка .env файла**
```bash
# Переименуйте .env_beget в .env
mv .env_beget .env

# Проверьте содержимое
cat .env
```

### 3. **Проверка прав доступа**
```bash
# Установите правильные права
sudo chown -R botuser:botuser /home/botuser/dating_bot
chmod +x /home/botuser/dating_bot/main.py
```

### 4. **Тестирование бота**
```bash
# Запустите бота вручную для тестирования
cd /home/botuser/dating_bot
source venv/bin/activate
python main.py
```

### 5. **Запуск через systemd**
```bash
# Запустите сервис
sudo systemctl start dating-bot

# Проверьте статус
sudo systemctl status dating-bot

# Проверьте логи
sudo journalctl -u dating-bot -f
```

## 🔍 Проверка работы

### **Тест бота**
1. Найдите вашего бота в Telegram
2. Отправьте команду `/start`
3. Проверьте, что бот отвечает

### **Проверка логов**
```bash
# Логи systemd
sudo journalctl -u dating-bot -n 50

# Логи приложения
tail -f /home/botuser/dating_bot/logs/dating_bot.log
```

### **Проверка ресурсов**
```bash
# Использование CPU и памяти
htop

# Использование диска
df -h

# Процессы Python
ps aux | grep python
```

## 🆘 Если что-то не работает

### **Бот не запускается**
```bash
# Проверьте логи
sudo journalctl -u dating-bot -n 50

# Проверьте права доступа
ls -la /home/botuser/dating_bot/

# Проверьте Python
python3 --version
```

### **Ошибки зависимостей**
```bash
# Переустановите зависимости
cd /home/botuser/dating_bot
source venv/bin/activate
pip install --force-reinstall -r requirements.txt
```

### **Проблемы с базой данных**
```bash
# Проверьте файл базы данных
ls -la /home/botuser/dating_bot/dating_bot.db

# Проверьте права доступа
sudo chown botuser:botuser /home/botuser/dating_bot/dating_bot.db
```

## 📊 Управление ботом

### **Основные команды**
```bash
# Статус бота
/home/botuser/manage_bot.sh status

# Запуск бота
/home/botuser/manage_bot.sh start

# Остановка бота
/home/botuser/manage_bot.sh stop

# Перезапуск бота
/home/botuser/manage_bot.sh restart

# Просмотр логов
/home/botuser/manage_bot.sh logs

# Обновление бота
/home/botuser/manage_bot.sh update

# Создание бэкапа
/home/botuser/manage_bot.sh backup
```

## 🎯 Готово!

После выполнения всех шагов ваш бот будет работать на Ubuntu VPS!

### **Преимущества VPS:**
- ✅ Полный контроль над сервером
- ✅ Лучшая производительность
- ✅ Возможность масштабирования
- ✅ Профессиональная настройка
- ✅ Автоматический перезапуск
- ✅ Мониторинг и логирование 