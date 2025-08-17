#!/usr/bin/env python3
import os
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler

print("=== ЗАПУСК ПРОСТОГО СЕРВЕРА ===")
print(f"Python: {sys.version}")
print(f"Директория: {os.getcwd()}")
print(f"Файлы: {os.listdir('.')}")
print(f"PORT: {os.environ.get('PORT', 'НЕ УСТАНОВЛЕН')}")

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(f"Получен запрос: {self.path}")
        
        if self.path in ['/', '/health']:
            self.send_response(200)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            response = "OK - Сервер работает!"
            self.wfile.write(response.encode('utf-8'))
            print("Отправлен ответ: 200 OK")
        else:
            self.send_response(404)
            self.end_headers()
            print("Отправлен ответ: 404")

    def log_message(self, format, *args):
        print(f"HTTP: {format % args}")

def main():
    try:
        port = int(os.environ.get("PORT", 8000))
        print(f"Запуск сервера на порту {port}")
        
        server = HTTPServer(('0.0.0.0', port), SimpleHandler)
        print(f"Сервер запущен на 0.0.0.0:{port}")
        
        server.serve_forever()
    except Exception as e:
        print(f"Ошибка: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main() 