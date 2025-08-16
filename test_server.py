#!/usr/bin/env python3
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestHandler(BaseHTTPRequestHandler):
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

def main():
    try:
        port = int(os.environ.get("PORT", 8000))
        logger.info(f"🚀 Запуск тестового сервера на порту {port}")
        
        server = HTTPServer(('0.0.0.0', port), TestHandler)
        logger.info(f"✅ Сервер запущен на http://0.0.0.0:{port}")
        
        server.serve_forever()
    except Exception as e:
        logger.error(f"❌ Ошибка запуска сервера: {e}")
        raise

if __name__ == "__main__":
    main() 