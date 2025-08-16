#!/usr/bin/env python3
import subprocess
import sys
import os
import time
import threading

def run_bot():
    """Запуск бота в отдельном процессе"""
    try:
        subprocess.run([sys.executable, "main_railway.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Ошибка запуска бота: {e}")
    except KeyboardInterrupt:
        print("Бот остановлен")

def main():
    print("🚀 Запуск бота в фоне...")
    
    # Запускаем бота в отдельном потоке
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    print("✅ Бот запущен в фоне")
    
    # Ждем немного, чтобы бот успел запуститься
    time.sleep(5)
    
    # Запускаем веб-сервер
    print("🌐 Запуск веб-сервера...")
    subprocess.run([sys.executable, "web_server.py"])

if __name__ == "__main__":
    main()
