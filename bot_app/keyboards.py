from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database import requests as rq

main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Зарегистрировать почтовый ящик", callback_data='registration')],
    [InlineKeyboardButton(text="Список почтовых ящиков", callback_data='checking_mailboxes')]
])


async def inline_mailboxes(chat_id: int):
    keyboard = InlineKeyboardBuilder()
    posts = await rq.get_mailboxes(chat_id)
    for post in posts:
        print(post.email)
        keyboard.add(InlineKeyboardButton(text=f'{post.email}', callback_data=f'check_{post.mailbox_id}'))
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data='start'))
    return keyboard.adjust(1).as_markup()
