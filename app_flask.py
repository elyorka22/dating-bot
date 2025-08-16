#!/usr/bin/env python3
import os
import sys
import logging
from flask import Flask

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    force=True
)
logger = logging.getLogger(__name__)

print("=== ЗАПУСК FLASK APP ===")
print(f"Python версия: {sys.version}")
print(f"Текущая директория: {os.getcwd()}")
print(f"Файлы в директории: {os.listdir('.')}")
print(f"PORT: {os.environ.get('PORT', 'НЕ УСТАНОВЛЕН')}")

app = Flask(__name__)

@app.route('/')
def home():
    print("Запрос на /")
    logger.info("Запрос на /")
    return "Bot is running! Status: OK"

@app.route('/health')
def health():
    print("Запрос на /health")
    logger.info("Запрос на /health")
    return "OK"

@app.route('/status')
def status():
    print("Запрос на /status")
    logger.info("Запрос на /status")
    return "Bot is running!"

if __name__ == '__main__':
    try:
        port = int(os.environ.get("PORT", 8000))
        print(f"🚀 Запуск Flask сервера на порту {port}")
        logger.info(f"🚀 Запуск Flask сервера на порту {port}")
        
        # Запускаем Flask
        app.run(host='0.0.0.0', port=port, debug=False)
        
    except Exception as e:
        print(f"❌ Ошибка запуска Flask: {e}")
        logger.error(f"❌ Ошибка запуска Flask: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1) 