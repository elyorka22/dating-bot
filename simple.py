#!/usr/bin/env python3
import os
import sys
import time

print("=== МАКСИМАЛЬНО ПРОСТАЯ ВЕРСИЯ ===")
print(f"Python версия: {sys.version}")
print(f"Текущая директория: {os.getcwd()}")
print(f"Файлы в директории: {os.listdir('.')}")
print(f"PORT: {os.environ.get('PORT', 'НЕ УСТАНОВЛЕН')}")

# Ждем 5 секунд для инициализации
print("Ждем 5 секунд для инициализации...")
time.sleep(5)
print("Инициализация завершена")

try:
    from http.server import HTTPServer, BaseHTTPRequestHandler
    print("HTTP сервер импортирован успешно")
except Exception as e:
    print(f"Ошибка импорта HTTP сервера: {e}")
    sys.exit(1)

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(f"Получен запрос: {self.path}")
        
        try:
            # Отвечаем на любой запрос
            self.send_response(200)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            response = f"OK - Сервер работает! Запрос: {self.path}"
            self.wfile.write(response.encode('utf-8'))
            print(f"Отправлен ответ: 200 OK для {self.path}")
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
        port = int(os.environ.get("PORT", 8000))
        print(f"Порт: {port}")
        
        print("Создание сервера...")
        server = HTTPServer(('0.0.0.0', port), SimpleHandler)
        print(f"Сервер создан на 0.0.0.0:{port}")
        
        print("Запуск сервера...")
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