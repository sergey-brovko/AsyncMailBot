from aiogram import Bot
from database import requests as rq
from database.mongodb import write_html
from mailboxes.media import files_to_media
from mailboxes.mail import MailFilter
from bot_app.keyboards import web_app_kb
import asyncio
from dotenv import load_dotenv
import os
import logging

logger2 = logging.getLogger(__name__)
logger2.setLevel(logging.DEBUG)
handler2 = logging.FileHandler(f"{__name__}.log", mode='w')
formatter2 = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
handler2.setFormatter(formatter2)
logger2.addHandler(handler2)
logger2.info(f"Testing the custom logger for module {__name__}...")

load_dotenv()


async def send_emails() -> None:
    async with Bot(token=os.getenv('TOKEN')) as bot:
        while True:
            try:
                mailboxes_rules = await rq.get_all_rules()
                for mailbox, rules in mailboxes_rules:
                    mail = MailFilter(mailbox['email'], mailbox['password'], rules=rules)
                    messages = mail.get_response()
                    if messages:
                        for msg in messages:
                            if msg['type'] == 'all':
                                html = msg['data']
                                html_id = f"{mailbox['chat_id']}-{html.get('mail_id')}"
                                await write_html(html_id, html['html'])
                                await bot.send_message(chat_id=mailbox['chat_id'], text=f'Входящее письмо '
                                                                                        f'\nдля "{mailbox['email']}"',
                                                       reply_markup=await web_app_kb(html_id))
                            elif msg['type'] == 'file':
                                files = msg['data']
                                for file in files:
                                    await bot.send_media_group(chat_id=mailbox['chat_id'], media=[files_to_media(file)])
                                await bot.send_message(chat_id=mailbox['chat_id'], text=f'Получено {len(files)} файл-а(-ов)'
                                                                                        f'\nдля "{mailbox['email']}"')
                            elif msg['type'] == 'text':
                                text = msg['data']
                                await bot.send_message(chat_id=mailbox['chat_id'], text=f'Входящее письмо \nдля '
                                                                                        f'"{mailbox['email']}"\n{text}')

            except Exception as e:
                logger2.exception(f"Ошибка модуля проверки почты.", exc_info=e)
            finally:
                await asyncio.sleep(5)


def mail_worker():
    try:
        asyncio.run(send_emails())
        logger2.info('Включено отслеживание входящей почты остановлено')
    except KeyboardInterrupt:
        logger2.exception('Отслеживание входящей почты остановлено')

