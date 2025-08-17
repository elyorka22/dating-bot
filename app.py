#!/usr/bin/env python3
import os
import sys
import time

print("=== FLASK ВЕРСИЯ - НАЧАЛО ===")
print(f"Python версия: {sys.version}")
print(f"Текущая директория: {os.getcwd()}")
print(f"Файлы в директории: {os.listdir('.')}")
print(f"PORT: {os.environ.get('PORT', 'НЕ УСТАНОВЛЕН')}")

# Ждем немного
time.sleep(2)
print("Пауза завершена")

try:
    from flask import Flask
    print("Flask импортирован успешно")
except Exception as e:
    print(f"Ошибка импорта Flask: {e}")
    sys.exit(1)

app = Flask(__name__)

@app.route('/')
def home():
    print("Запрос на /")
    return "OK - Flask сервер работает!"

@app.route('/health')
def health():
    print("Запрос на /health")
    return "OK"

if __name__ == '__main__':
    print("=== ЗАПУСК FLASK ===")
    try:
        port = int(os.environ.get("PORT", 8000))
        print(f"Запуск Flask на порту {port}")
        app.run(host='0.0.0.0', port=port, debug=False)
    except Exception as e:
        print(f"Ошибка запуска Flask: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1) 