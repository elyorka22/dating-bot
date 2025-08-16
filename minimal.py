#!/usr/bin/env python3
import os
import sys
import socket

print("=== МИНИМАЛЬНЫЙ ТЕСТ ===")
print(f"Python: {sys.version}")
print(f"Директория: {os.getcwd()}")
print(f"Файлы: {os.listdir('.')}")
print(f"PORT: {os.environ.get('PORT', 'НЕ УСТАНОВЛЕН')}")

# Создаем простой TCP сервер
port = int(os.environ.get("PORT", 8000))
print(f"Запуск TCP сервера на порту {port}")

try:
    # Создаем сокет
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('0.0.0.0', port))
    sock.listen(5)
    
    print(f"✅ Сервер запущен на 0.0.0.0:{port}")
    
    while True:
        conn, addr = sock.accept()
        print(f"Подключение от {addr}")
        
        # Простой HTTP ответ
        response = "HTTP/1.1 200 OK\r\n"
        response += "Content-Type: text/plain\r\n"
        response += "Content-Length: 19\r\n"
        response += "\r\n"
        response += "Bot is running!"
        
        conn.send(response.encode())
        conn.close()
        
except Exception as e:
    print(f"Ошибка: {e}")
    import traceback
    traceback.print_exc() 