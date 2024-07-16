from aiogram import Bot
from database import requests as rq
from database.mongodb import write_html
from mailboxes.media import files_to_media
from mailboxes.mail import MailFile, MailText, MailHtml
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
            rules = await rq.get_all_rules()
            for rule in rules:
                if rule[1] == 'all':
                    mail = MailHtml(email=rule[2], password=rule[3], from_email=rule[0])
                    html = await mail.get_response()
                    if html:
                        html_id = f"{rule[4]}-{html.get('mail_id')}"
                        await write_html(html_id, html['html'])
                        await bot.send_message(chat_id=rule[4], text=f'Входящее письмо от "{rule[0]}" для "{rule[2]}"',
                                               reply_markup=await web_app_kb(html_id))
                elif rule[1] == 'file':
                    mail = MailFile(email=rule[2], password=rule[3], from_email=rule[0])
                    files = await mail.get_response()
                    if files:
                        for file in files:
                            await bot.send_media_group(chat_id=rule[4], media=[files_to_media(file)])
                        await bot.send_message(chat_id=rule[4], text=f'Получено {len(files)} файл-а(-ов) от "{rule[0]}"'
                                                                     f' для "{rule[2]}"')
                elif rule[1] == 'text':
                    mail = MailText(email=rule[2], password=rule[3], from_email=rule[0])
                    text = await mail.get_response()
                    if text:
                        await bot.send_message(chat_id=rule[4], text=f'Входящее письмо от "{rule[0]}" для "{rule[2]}"\n'
                                                                     f'{text}')
            await asyncio.sleep(5)


def mail_worker():
    try:
        asyncio.run(send_emails())
        logger2.info('Включено отслеживание входящей почты остановлено')
    except KeyboardInterrupt:
        logger2.exception('Отслеживание входящей почты остановлено')

