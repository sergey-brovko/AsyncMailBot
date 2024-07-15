import os
from dotenv import load_dotenv
from database.models import async_main
from bot_app.handlers import router
import asyncio
from aiogram import Bot, Dispatcher
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler(f"{__name__}.log", mode='w')
formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.info(f"Testing the custom logger for module {__name__}...")

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
        logger.info('Бот включен')
    except KeyboardInterrupt:
        logger.exception('Бот выключен')
