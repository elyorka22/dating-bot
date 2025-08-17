#!/usr/bin/env python3
import os
import sys
import time
import requests
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

print("=== ЗАПУСК БОТА ===")
print(f"Python версия: {sys.version}")
print(f"Текущая директория: {os.getcwd()}")
print(f"Файлы в директории: {os.listdir('.')}")
print(f"PORT: {os.environ.get('PORT', 'НЕ УСТАНОВЛЕН')}")

# Токен бота
BOT_TOKEN = os.getenv("BOT_TOKEN", "8256818214:AAFwnmIc-pKeN8IgpkrW15B6TpUDVdS4ZKI")

def get_bot_info():
    """Получение информации о боте"""
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getMe"
        response = requests.get(url)
        if response.status_code == 200:
            bot_info = response.json()
            print(f"Бот: {bot_info['result']['first_name']} (@{bot_info['result']['username']})")
            return True
        else:
            print(f"Ошибка получения информации о боте: {response.status_code}")
            return False
    except Exception as e:
        print(f"Ошибка получения информации о боте: {e}")
        return False

def run_bot():
    """Запуск бота в фоне"""
    print("🤖 Запуск бота...")
    
    # Проверяем информацию о боте
    if get_bot_info():
        print("✅ Бот подключен к Telegram API")
    else:
        print("❌ Ошибка подключения к Telegram API")
        return
    
    # Простой цикл для поддержания бота активным
    while True:
        try:
            time.sleep(60)  # Проверяем каждую минуту
            print("Бот активен...")
        except KeyboardInterrupt:
            print("Бот остановлен")
            break
        except Exception as e:
            print(f"Ошибка в цикле бота: {e}")
            time.sleep(10)

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(f"Получен запрос: {self.path}")
        
        try:
            if self.path in ['/', '/health']:
                self.send_response(200)
                self.send_header('Content-type', 'text/plain; charset=utf-8')
                self.end_headers()
                response = "OK - Бот работает!"
                self.wfile.write(response.encode('utf-8'))
                print(f"Отправлен ответ: 200 OK для {self.path}")
            else:
                self.send_response(404)
                self.end_headers()
                print("Отправлен ответ: 404")
        except Exception as e:
            print(f"Ошибка в обработке запроса: {e}")
            try:
                self.send_response(500)
                self.end_headers()
            except:
                pass

    def log_message(self, format, *args):
        print(f"HTTP: {format % args}")

def main():
    print("=== НАЧАЛО MAIN ===")
    
    try:
        # Запускаем бота в отдельном потоке
        bot_thread = threading.Thread(target=run_bot, daemon=True)
        bot_thread.start()
        print("✅ Бот запущен в фоне")
        
        # Ждем немного, чтобы бот успел запуститься
        time.sleep(3)
        
        # Запускаем веб-сервер
        port = int(os.environ.get("PORT", 8000))
        print(f"Порт: {port}")
        
        print("Создание веб-сервера...")
        server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
        print(f"Веб-сервер создан на 0.0.0.0:{port}")
        
        print("Запуск веб-сервера...")
        print("Сервер готов принимать запросы!")
        server.serve_forever()
        
    except Exception as e:
        print(f"Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    print("=== ТОЧКА ВХОДА ===")
    main() 