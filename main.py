#!/usr/bin/env python3
import os
import sys
import time

print("=== НАЧАЛО ЗАПУСКА ===")
print(f"Python версия: {sys.version}")
print(f"Текущая директория: {os.getcwd()}")
print(f"Файлы в директории: {os.listdir('.')}")
print(f"PORT: {os.environ.get('PORT', 'НЕ УСТАНОВЛЕН')}")

# Ждем немного, чтобы убедиться, что все загрузилось
time.sleep(2)
print("Пауза завершена")

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
        except Exception as e:
            print(f"Ошибка в обработке запроса: {e}")
            self.send_response(500)
            self.end_headers()

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
        server.serve_forever()
        
    except Exception as e:
        print(f"Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    print("=== ТОЧКА ВХОДА ===")
    main() 