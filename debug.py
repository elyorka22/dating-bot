#!/usr/bin/env python3
import os
import sys

print("=== ОТЛАДКА СИСТЕМЫ ===")
print(f"Python версия: {sys.version}")
print(f"Python путь: {sys.executable}")
print(f"Текущая директория: {os.getcwd()}")
print(f"Содержимое директории: {os.listdir('.')}")

print("\n=== ПЕРЕМЕННЫЕ ОКРУЖЕНИЯ ===")
print(f"PORT: {os.environ.get('PORT', 'НЕ УСТАНОВЛЕН')}")
print(f"BOT_TOKEN: {'УСТАНОВЛЕН' if os.environ.get('BOT_TOKEN') else 'НЕ УСТАНОВЛЕН'}")

print("\n=== ПРОВЕРКА ФАЙЛОВ ===")
files_to_check = ['app.py', 'requirements.txt', 'Procfile']
for file in files_to_check:
    if os.path.exists(file):
        print(f"✅ {file} - существует")
        with open(file, 'r') as f:
            content = f.read()
            print(f"   Размер: {len(content)} символов")
    else:
        print(f"❌ {file} - НЕ НАЙДЕН")

print("\n=== ГОТОВ К РАБОТЕ ===") 