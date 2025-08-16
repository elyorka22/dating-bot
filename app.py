#!/usr/bin/env python3
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        logger.info(f"GET запрос: {self.path}")
        
        if self.path in ['/', '/health', '/status']:
            self.send_response(200)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            response = "OK - Bot is running!"
            self.wfile.write(response.encode('utf-8'))
            logger.info("Отправлен ответ: 200 OK")
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            response = "Not Found"
            self.wfile.write(response.encode('utf-8'))
            logger.info("Отправлен ответ: 404 Not Found")
    
    def log_message(self, format, *args):
        logger.info(f"HTTP: {format % args}")

def main():
    try:
        # Получаем порт из переменной окружения Railway
        port = int(os.environ.get("PORT", 8000))
        logger.info(f"🚀 Запуск сервера на порту {port}")
        
        # Создаем сервер
        server = HTTPServer(('0.0.0.0', port), SimpleHandler)
        logger.info(f"✅ Сервер создан на 0.0.0.0:{port}")
        
        # Запускаем сервер
        logger.info("🌐 Сервер запускается...")
        server.serve_forever()
        
    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}")
        raise

if __name__ == "__main__":
    main() 