from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Зарегистрировать почтовый ящик", callback_data='registration')],
    [InlineKeyboardButton(text="Список почтовых ящиков", callback_data='checking_mailboxes')]
])

posts = ['dsad@hay.fd', '1@mail.ru', 'cdswfw@ya.ru']


async def inline_posts():
    keyboard = InlineKeyboardBuilder()
    for post in posts:
        keyboard.add(InlineKeyboardButton(text=post, callback_data='check'))
    keyboard.add(InlineKeyboardButton(text='Назад', ))
    return keyboard.adjust(1).as_markup()
