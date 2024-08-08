from aiogram import Bot
from database import requests as rq
from database.mongodb import write_html
from media import files_to_media
from mail import MailFilter
from keyboards import web_app_kb
from database.models import async_main
import asyncio
from dotenv import load_dotenv
import os
import logging

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

load_dotenv()


async def send_emails() -> None:
    await async_main()
    async with Bot(token=os.getenv('TOKEN')) as bot:
        while True:
            try:
                mailboxes_rules = await rq.get_all_rules()
                for mailbox, rules in mailboxes_rules:
                    mail = MailFilter(mailbox['email'], mailbox['password'], rules=rules)
                    messages = mail.get_response()
                    del mail
                    if messages:
                        for msg in messages:
                            if msg['type'] == 'all':
                                html = msg['data']
                                html_id = f"{mailbox['chat_id']}-{html.get('mail_id')}"
                                await write_html(html_id, html['html'])
                                await bot.send_message(chat_id=mailbox['chat_id'],
                                                       text=f'Входящее письмо \nдля "{mailbox['email']}"'
                                                            f'\nот "{html['from']}"',
                                                       reply_markup=await web_app_kb(html_id))
                            elif msg['type'] == 'file':
                                files = msg['data']['files']
                                for file in files:
                                    await bot.send_media_group(chat_id=mailbox['chat_id'], media=[files_to_media(file)])
                                await bot.send_message(chat_id=mailbox['chat_id'],
                                                       text=f'Получено {len(files)} файл-а(-ов)\nдля "{mailbox['email']}'
                                                            f'"\nот "{msg['data']['from']}"')
                            elif msg['type'] == 'text':
                                text = msg['data']['text']
                                await bot.send_message(chat_id=mailbox['chat_id'],
                                                       text=f'Входящее письмо \nдля "{mailbox['email']}"\n{text}\nот '
                                                            f'"{msg['data']['from']}"')
            except Exception as e:
                logger.exception(f"Ошибка модуля проверки почты.", exc_info=e)
            finally:
                await asyncio.sleep(5)


if __name__ == '__main__':
    try:
        asyncio.run(send_emails())
        logger.info('Включено отслеживание входящей почты остановлено')
    except KeyboardInterrupt:
        logger.exception('Отслеживание входящей почты остановлено')

