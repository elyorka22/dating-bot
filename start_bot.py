#!/usr/bin/env python3
# Скрипт запуска для Beget
import os
import sys

# Добавляем путь к проекту
project_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_path)

# Импортируем и запускаем бота
from main import main
import asyncio

if __name__ == "__main__":
    asyncio.run(main())
