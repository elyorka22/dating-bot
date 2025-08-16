#!/usr/bin/env python3
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import logging
import requests
import time

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Токен бота
BOT_TOKEN = os.getenv("BOT_TOKEN", "8256818214:AAFwnmIc-pKeN8IgpkrW15B6TpUDVdS4ZKI")

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        logger.info(f"Получен запрос: {self.path}")
        
        if self.path in ['/', '/health']:
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            response = "Bot is running! Status: OK"
            self.wfile.write(response.encode())
            logger.info("Отправлен ответ: 200 OK")
        else:
            self.send_response(404)
            self.end_headers()
            logger.info("Отправлен ответ: 404 Not Found")
    
    def log_message(self, format, *args):
        logger.info(f"HTTP: {format % args}")

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

def run_web_server():
    """Запуск веб-сервера"""
    try:
        port = int(os.environ.get("PORT", 8000))
        logger.info(f"🌐 Запуск веб-сервера на порту {port}")
        
        server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
        logger.info(f"✅ Веб-сервер запущен на http://0.0.0.0:{port}")
        
        server.serve_forever()
    except Exception as e:
        logger.error(f"❌ Ошибка запуска веб-сервера: {e}")
        raise

def main():
    logger.info("🚀 Запуск комбинированного сервера...")
    
    # Запускаем бота в отдельном потоке
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    logger.info("✅ Бот запущен в фоне")
    
    # Ждем немного, чтобы бот успел запуститься
    time.sleep(3)
    
    # Запускаем веб-сервер в основном потоке
    run_web_server()

if __name__ == "__main__":
    main() 