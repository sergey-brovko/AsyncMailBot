import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import os
from database.models import async_main
from bot_app.handlers import router
from multiprocessing import Process
from mailboxes.catch_email import worker
load_dotenv()


async def main():
    bot = Bot(token=os.getenv('TOKEN'))
    await async_main()
    process = Process(target=worker)
    process.start()
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)
    process.join()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')
