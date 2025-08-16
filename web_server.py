#!/usr/bin/env python3
import os
import asyncio
from aiohttp import web
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def healthcheck_handler(request):
    """Обработчик для healthcheck"""
    return web.Response(text="Bot is running!", status=200)

async def main():
    """Запуск веб-сервера"""
    app = web.Application()
    app.router.add_get('/', healthcheck_handler)
    app.router.add_get('/health', healthcheck_handler)
    
    port = int(os.environ.get("PORT", 8000))
    logger.info(f"🌐 Запуск веб-сервера на порту {port}")
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    
    logger.info(f"✅ Веб-сервер запущен на http://0.0.0.0:{port}")
    
    # Держим сервер запущенным
    try:
        await asyncio.Future()  # Бесконечное ожидание
    except KeyboardInterrupt:
        logger.info("Остановка веб-сервера...")
    finally:
        await runner.cleanup()

if __name__ == "__main__":
    asyncio.run(main()) 