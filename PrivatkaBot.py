import asyncio
from aiogram import Bot, Dispatcher
from app.handlers import router
import time


bot = Bot(token="")

async def main():
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        print("[INFO] Инициализация токена бота...")
        time.sleep(1)
        print("[INFO] Подключение диспетчера...")
        time.sleep(1)
        print("[INFO] Подключение роутера...")
        time.sleep(2)
        print("[SUCCESS] Бот успешно включен")
        asyncio.run(main())
    except KeyboardInterrupt:
        print("[INFO] Бот отключен")