#!/usr/bin/env python3
import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running! Status: OK"

@app.route('/health')
def health():
    return "OK"

@app.route('/status')
def status():
    return "Bot is running!"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    print(f"🚀 Запуск Flask сервера на порту {port}")
    app.run(host='0.0.0.0', port=port, debug=False) 