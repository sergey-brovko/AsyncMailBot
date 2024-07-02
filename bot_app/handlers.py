from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters.command import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from database import requests as rq
from bot_app import keyboards as kb

router = Router()


class RegMailbox(StatesGroup):
    email = State()
    password = State()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await rq.set_user(message.chat.id)
    await message.answer(f"Приветствую, {message.from_user.first_name}, выберите одно из "
                         f"доступных действий", reply_markup=kb.main)


@router.callback_query(F.data == 'registration')
async def registration(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Введите данные для регистрации почтового ящика')
    await state.set_state(RegMailbox.email)
    await callback.message.edit_text('Введите имя почтового ящика:')


@router.message(RegMailbox.email)
async def enter_password(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    await state.set_state(RegMailbox.password)
    await message.answer("Введите пароль от почтового ящика:")


@router.message(RegMailbox.password)
async def finish_registration(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    data = await state.get_data()
    try:
        await rq.set_mailbox(chat_id=message.chat.id, email=data['email'], password=data['password'])
        await message.answer("Почтовый ящик зарегистрирован")
    except Exception as e:
        await message.answer(f"Ошибка при регистрации:\n{e}")
    finally:
        await state.clear()
        await cmd_start(message)


@router.callback_query(F.data == 'checking_mailboxes')
async def registration(callback: CallbackQuery):
    await callback.answer('Список ваших почтовых ящиков')
    await callback.message.edit_text('Список ваших почтовых ящиков',
                                     reply_markup=await kb.inline_mailboxes(callback.message.chat.id))


@router.callback_query(F.data == 'start')
async def start(callback: CallbackQuery):
    await callback.answer('Главное меню')
    await callback.message.edit_text(f"Выберите одно из доступных действий",
                                     reply_markup=kb.main)


@router.callback_query(F.data == 'mailbox_')
async def start(callback: CallbackQuery):

    await callback.answer('Главное меню')
    await callback.message.edit_text(f"Выберите одно из доступных действий",
                                     reply_markup=kb.main)
