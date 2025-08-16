#!/usr/bin/env python3
import os
import sys

print("=== ТЕСТОВЫЙ ФАЙЛ ===")
print(f"Python: {sys.version}")
print(f"Директория: {os.getcwd()}")
print(f"Файлы: {os.listdir('.')}")
print(f"PORT: {os.environ.get('PORT', 'НЕ УСТАНОВЛЕН')}")

# Простой HTTP сервер
from http.server import HTTPServer, BaseHTTPRequestHandler

class TestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(f"Запрос: {self.path}")
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"TEST OK")

port = int(os.environ.get("PORT", 8000))
print(f"Запуск на порту {port}")

server = HTTPServer(('0.0.0.0', port), TestHandler)
print("Сервер запущен!")
server.serve_forever() 