from aiogram import Bot
from aiogram.types import BufferedInputFile
from database import requests as rq
from mailboxes.mail import MailFile, MailText
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()


async def send_emails() -> None:
    while True:
        async with Bot(token=os.getenv('TOKEN')) as bot:
            rules = await rq.get_all_rules()
            print(len(rules))
            for rule in rules:
                if rule[1] == 'all':
                    pass
                elif rule[1] == 'file':
                    mail = MailFile(email=rule[2], password=rule[3], from_email=rule[0])
                    files = mail.get_response()
                    if files:
                        for name, file in files:
                            await bot.send_document(chat_id=rule[4],
                                                    document=BufferedInputFile(file=file, filename=name), caption=name)
                elif rule[1] == 'text':
                    mail = MailText(email=rule[2], password=rule[3], from_email=rule[0])
                    text = mail.get_response()
                    if text:
                        await bot.send_message(chat_id=rule[4], text=text)
        await asyncio.sleep(5)


def worker():
    try:
        asyncio.run((send_emails()))
    except KeyboardInterrupt:
        print('Отслеживание входящей почты остановлено')

