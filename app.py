#!/usr/bin/env python3
import os
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
import logging

# Принудительная настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    force=True
)
logger = logging.getLogger(__name__)

print("=== ЗАПУСК APP.PY ===")
print(f"Python версия: {sys.version}")
print(f"Текущая директория: {os.getcwd()}")
print(f"Файлы в директории: {os.listdir('.')}")

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(f"GET запрос: {self.path}")
        logger.info(f"GET запрос: {self.path}")
        
        if self.path in ['/', '/health', '/status']:
            self.send_response(200)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            response = "OK - Bot is running!"
            self.wfile.write(response.encode('utf-8'))
            print("Отправлен ответ: 200 OK")
            logger.info("Отправлен ответ: 200 OK")
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            response = "Not Found"
            self.wfile.write(response.encode('utf-8'))
            print("Отправлен ответ: 404 Not Found")
            logger.info("Отправлен ответ: 404 Not Found")
    
    def log_message(self, format, *args):
        print(f"HTTP: {format % args}")
        logger.info(f"HTTP: {format % args}")

def main():
    try:
        print("=== НАЧАЛО MAIN ===")
        
        # Получаем порт из переменной окружения Railway
        port = int(os.environ.get("PORT", 8000))
        print(f"Порт: {port}")
        logger.info(f"🚀 Запуск сервера на порту {port}")
        
        # Создаем сервер
        print("Создание сервера...")
        server = HTTPServer(('0.0.0.0', port), SimpleHandler)
        print(f"✅ Сервер создан на 0.0.0.0:{port}")
        logger.info(f"✅ Сервер создан на 0.0.0.0:{port}")
        
        # Запускаем сервер
        print("🌐 Сервер запускается...")
        logger.info("🌐 Сервер запускается...")
        server.serve_forever()
        
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        logger.error(f"❌ Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()
        raise

if __name__ == "__main__":
    print("=== ТОЧКА ВХОДА ===")
    main() 