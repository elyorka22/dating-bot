#!/usr/bin/env python3
import os
import logging
import requests
import time
import threading

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Токен бота
BOT_TOKEN = os.getenv("BOT_TOKEN", "8256818214:AAFwnmIc-pKeN8IgpkrW15B6TpUDVdS4ZKI")

def send_telegram_message(chat_id, text):
    """Отправка сообщения в Telegram"""
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": text
        }
        response = requests.post(url, data=data)
        if response.status_code == 200:
            logger.info(f"Сообщение отправлено в {chat_id}")
            return True
        else:
            logger.error(f"Ошибка отправки: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"Ошибка отправки сообщения: {e}")
        return False

def get_bot_info():
    """Получение информации о боте"""
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getMe"
        response = requests.get(url)
        if response.status_code == 200:
            bot_info = response.json()
            logger.info(f"Бот: {bot_info['result']['first_name']} (@{bot_info['result']['username']})")
            return True
        else:
            logger.error(f"Ошибка получения информации о боте: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"Ошибка получения информации о боте: {e}")
        return False

def run_bot():
    """Запуск простого бота"""
    logger.info("🤖 Запуск простого бота...")
    
    # Проверяем информацию о боте
    if get_bot_info():
        logger.info("✅ Бот подключен к Telegram API")
    else:
        logger.error("❌ Ошибка подключения к Telegram API")
        return
    
    # Простой цикл для поддержания бота активным
    while True:
        try:
            time.sleep(60)  # Проверяем каждую минуту
            logger.info("Бот активен...")
        except KeyboardInterrupt:
            logger.info("Бот остановлен")
            break
        except Exception as e:
            logger.error(f"Ошибка в цикле бота: {e}")
            time.sleep(10)

def main():
    logger.info("🚀 Запуск простого бота...")
    
    # Запускаем бота в отдельном потоке
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    logger.info("✅ Бот запущен в фоне")
    
    # Ждем немного
    time.sleep(5)
    
    logger.info("Бот готов к работе!")

if __name__ == "__main__":
    main() 