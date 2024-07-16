import os
from dotenv import load_dotenv
from database.models import async_main
from bot_app.handlers import router
import asyncio
from aiogram import Bot, Dispatcher
import logging

logger1 = logging.getLogger(__name__)
logger1.setLevel(logging.DEBUG)
handler1 = logging.FileHandler(f"{__name__}.log", mode='w')
formatter1 = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
handler1.setFormatter(formatter1)
logger1.addHandler(handler1)
logger1.info(f"Testing the custom logger for module {__name__}...")

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
        logger1.info('Бот включен')
    except KeyboardInterrupt:
        logger1.exception('Бот выключен')
