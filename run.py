import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import os
from database.models import async_main
from bot_app.handlers import router
load_dotenv()


async def main():
    await async_main()
    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')