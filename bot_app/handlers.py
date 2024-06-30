from aiogram import Router
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from database import requests as rq


router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await rq.set_user(message.chat.id)
    btn1 = types.InlineKeyboardButton(text="Зарегистрировать почтовый ящик", callback_data='register')
    btn2 = types.InlineKeyboardButton(text="Список почтовых ящиков", callback_data='check')
    markup = types.InlineKeyboardMarkup(inline_keyboard=[[btn1], [btn2]])
    await message.answer(f"Приветствую, {message.from_user.first_name}, данный бот предназначен для "
                                          f"помощи в отслеживании важных писем вашей электронной почты. Выберите одно из "
                                          f"доступных действий", reply_markup=markup)


