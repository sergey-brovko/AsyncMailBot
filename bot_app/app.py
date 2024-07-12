import os
from dotenv import load_dotenv
from database.models import async_main
from bot_app.handlers import router
import asyncio
from aiogram import Bot, Dispatcher

load_dotenv()


async def main():
    bot = Bot(token=os.getenv('TOKEN'))
    await async_main()
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


def bot_run():
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')
