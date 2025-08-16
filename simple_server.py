#!/usr/bin/env python3
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import subprocess
import sys

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ['/', '/health']:
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"Bot is running!")
        else:
            self.send_response(404)
            self.end_headers()

def run_web_server():
    """Запуск веб-сервера"""
    port = int(os.environ.get("PORT", 8000))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    print(f"🌐 Веб-сервер запущен на порту {port}")
    server.serve_forever()

def run_bot():
    """Запуск бота"""
    try:
        subprocess.run([sys.executable, "main_railway.py"], check=True)
    except Exception as e:
        print(f"Ошибка запуска бота: {e}")

def main():
    print("🚀 Запуск бота и веб-сервера...")
    
    # Запускаем бота в отдельном потоке
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    print("✅ Бот запущен в фоне")
    
    # Запускаем веб-сервер в основном потоке
    run_web_server()

if __name__ == "__main__":
    main() 