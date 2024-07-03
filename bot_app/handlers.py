from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters.command import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from database import requests as rq
from bot_app import keyboards as kb
import mailboxes.mail as mb

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


@router.callback_query(F.data.startswith('mailbox_'))
async def mailbox_actions(callback: CallbackQuery):
    await callback.answer('Вы выбрали почтовый ящик')
    await callback.message.edit_text(f"Выберите действие",
                                     reply_markup=await kb.mailbox_menu(int(callback.data.split('_')[1])))


@router.callback_query(F.data.startswith('check_mailbox_'))
async def check_mailbox(callback: CallbackQuery):
    mailbox_id = int(callback.data.split('_')[2])
    mailbox = await rq.get_mailboxes_by_id(mailbox_id)
    text = ("Подключено"
            if await mb.Mail(email=mailbox.email, password=mailbox.password).is_connect()
            else "Не удалось подключиться. проверьте настройки почтового ящика (правильный логин и пароль, разрешение "
                 "в настройках почтового ящика для работы с IMAP)")
    await callback.answer('Проверка соединения с сервером')
    await callback.message.edit_text(text=text, reply_markup=await kb.mailbox_checking(mailbox_id))


@router.callback_query(F.data.startswith('delete_mailbox_'))
async def delete_mailbox(callback: CallbackQuery):
    mailbox_id = int(callback.data.split('_')[2])
    await rq.delete_mailbox_by_id(mailbox_id)
    await callback.answer('Почтовый ящик удален')
    await start(callback)
