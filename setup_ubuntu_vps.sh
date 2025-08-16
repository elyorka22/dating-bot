#!/bin/bash
# Скрипт автоматической настройки Ubuntu VPS для Telegram бота
# Запускайте от root пользователя

set -e  # Остановка при ошибке

echo "🚀 Настройка Ubuntu VPS для Telegram бота"
echo "=========================================="

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Функция для вывода с цветом
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Проверка root прав
if [ "$EUID" -ne 0 ]; then
    print_error "Запустите скрипт от root пользователя"
    exit 1
fi

# 1. Обновление системы
print_status "Обновление системы..."
apt update && apt upgrade -y

# 2. Установка необходимых пакетов
print_status "Установка необходимых пакетов..."
apt install -y python3 python3-pip python3-venv git curl wget htop ufw nano

# 3. Создание пользователя для бота
print_status "Создание пользователя botuser..."
if id "botuser" &>/dev/null; then
    print_warning "Пользователь botuser уже существует"
else
    adduser --disabled-password --gecos "" botuser
    usermod -aG sudo botuser
    print_status "Пользователь botuser создан"
fi

# 4. Создание директории проекта
print_status "Создание директории проекта..."
mkdir -p /home/botuser/dating_bot
chown botuser:botuser /home/botuser/dating_bot

# 5. Создание systemd сервиса
print_status "Создание systemd сервиса..."
cat > /etc/systemd/system/dating-bot.service << EOF
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
EOF

# 6. Настройка firewall
print_status "Настройка firewall..."
ufw allow ssh
ufw allow 80
ufw allow 443
ufw --force enable

# 7. Создание скрипта бэкапа
print_status "Создание скрипта бэкапа..."
cat > /home/botuser/backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/home/botuser/backups"
mkdir -p $BACKUP_DIR

# Бэкап базы данных
if [ -f "/home/botuser/dating_bot/dating_bot.db" ]; then
    cp /home/botuser/dating_bot/dating_bot.db $BACKUP_DIR/dating_bot_$DATE.db
    echo "База данных скопирована: dating_bot_$DATE.db"
fi

# Бэкап логов
if [ -d "/home/botuser/dating_bot/logs" ]; then
    tar -czf $BACKUP_DIR/logs_$DATE.tar.gz /home/botuser/dating_bot/logs/
    echo "Логи скопированы: logs_$DATE.tar.gz"
fi

# Удаляем старые бэкапы (старше 7 дней)
find $BACKUP_DIR -name "*.db" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

echo "Бэкап завершен: $DATE"
EOF

chmod +x /home/botuser/backup.sh
chown botuser:botuser /home/botuser/backup.sh

# 8. Создание скрипта управления
print_status "Создание скрипта управления..."
cat > /home/botuser/manage_bot.sh << 'EOF'
#!/bin/bash
# Скрипт управления ботом

case "$1" in
    start)
        sudo systemctl start dating-bot
        echo "Бот запущен"
        ;;
    stop)
        sudo systemctl stop dating-bot
        echo "Бот остановлен"
        ;;
    restart)
        sudo systemctl restart dating-bot
        echo "Бот перезапущен"
        ;;
    status)
        sudo systemctl status dating-bot
        ;;
    logs)
        sudo journalctl -u dating-bot -f
        ;;
    update)
        sudo systemctl stop dating-bot
        cd /home/botuser/dating_bot
        source venv/bin/activate
        pip install -r requirements.txt
        sudo systemctl start dating-bot
        echo "Бот обновлен и перезапущен"
        ;;
    backup)
        /home/botuser/backup.sh
        ;;
    *)
        echo "Использование: $0 {start|stop|restart|status|logs|update|backup}"
        exit 1
        ;;
esac
EOF

chmod +x /home/botuser/manage_bot.sh
chown botuser:botuser /home/botuser/manage_bot.sh

# 9. Перезагрузка systemd
print_status "Перезагрузка systemd..."
systemctl daemon-reload

# 10. Включение автозапуска
print_status "Включение автозапуска..."
systemctl enable dating-bot

print_status "Настройка завершена!"
echo ""
echo "📋 Следующие шаги:"
echo "1. Загрузите файлы бота в /home/botuser/dating_bot/"
echo "2. Создайте .env файл с настройками"
echo "3. Установите зависимости: cd /home/botuser/dating_bot && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
echo "4. Запустите бота: sudo systemctl start dating-bot"
echo ""
echo "🔧 Управление ботом:"
echo "- Статус: /home/botuser/manage_bot.sh status"
echo "- Логи: /home/botuser/manage_bot.sh logs"
echo "- Перезапуск: /home/botuser/manage_bot.sh restart"
echo "- Бэкап: /home/botuser/manage_bot.sh backup"
echo ""
echo "📊 Мониторинг:"
echo "- Ресурсы: htop"
echo "- Диск: df -h"
echo "- Память: free -h" 