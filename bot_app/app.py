import os
from dotenv import load_dotenv
from bot_app.database.models import async_main
from bot_app.handlers import router
import asyncio
from aiogram import Bot, Dispatcher
import logging

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

load_dotenv()


async def main():
    bot = Bot(token=os.getenv('TOKEN'))
    await async_main()
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
        logger.info('Бот включен')
    except KeyboardInterrupt:
        logger.exception('Бот выключен')
