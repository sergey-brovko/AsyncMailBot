from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters.command import Command
from database import requests as rq
from bot_app import keyboards as kb

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await rq.set_user(message.chat.id)
    await message.answer(f"Приветствую, {message.from_user.first_name}, данный бот предназначен для "
                         f"помощи в отслеживании важных писем вашей электронной почты. Выберите одно из "
                         f"доступных действий", reply_markup=kb.main)


@router.callback_query(F.data == 'registration')
async def registration(callback: CallbackQuery):
    await callback.answer('Вы выбрали регистрацию почтового ящика', show_alert=True)
    await callback.message.edit_text('Вам необходимо ввести данные для авторизации своего почтового '
                                     'ящика. Для этого нажмите на соответствующую кнопку и введите значение.',
                                     reply_markup=await kb.inline_posts())


