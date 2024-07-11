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


class RegRule(StatesGroup):
    email = State()
    action = State()
    mailbox_id = State()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await rq.set_user(message.chat.id)
    await message.answer(f"Приветствую, {message.from_user.first_name}, выберите одно из "
                         f"доступных действий", reply_markup=kb.main)


@router.message(Command("start_bot"))
async def cmd_start_bot(message: Message):
    await rq.update_user_status(message.chat.id, True)
    await message.answer("Бот включен на отслеживание почты")


@router.message(Command("stop_bot"))
async def cmd_stop_bot(message: Message):
    await rq.update_user_status(message.chat.id, False)
    await message.answer("Отслеживание почты ботом отключено")


@router.message(Command("info"))
async def cmd_info(message: Message):
    await message.answer(f"Бот предназначен для отслеживания важной для вас информации из вашей электронной почты. "
                         f"Пароли ваших электронных ящиков, хранятся в шифрованном виде и недоступны, как для "
                         f"администратора бота, так и для третьих лиц. Вопросы, относительно работы бота можно задать "
                         f"@true_kapitan", reply_markup=kb.main_menu)


@router.callback_query(F.data == 'registration')
async def registration(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Введите данные для регистрации почтового ящика')
    await state.set_state(RegMailbox.email)
    await callback.message.edit_text('Введите имя почтового ящика:')


@router.message(RegMailbox.email)
async def enter_password(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    await state.set_state(RegMailbox.password)
    await message.delete()
    await message.answer("Введите пароль от почтового ящика:")


@router.message(RegMailbox.password)
async def finish_registration(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    data = await state.get_data()
    await message.delete()
    try:
        await rq.set_mailbox(chat_id=message.chat.id, email=data['email'], password=data['password'])
        await message.answer("Почтовый ящик зарегистрирован")
    except Exception as e:
        await message.answer(f"Ошибка при регистрации:\n{e}")
    finally:
        await state.clear()
        await message.answer(f"Выберите одно из доступных действий", reply_markup=kb.main)


@router.callback_query(F.data == 'checking_mailboxes')
async def checking_mailboxes(callback: CallbackQuery):
    await callback.answer('Список ваших почтовых ящиков')
    await callback.message.edit_text('Список ваших почтовых ящиков',
                                     reply_markup=await kb.inline_mailboxes(callback.message.chat.id))


@router.callback_query(F.data == 'start')
async def start(callback: CallbackQuery):
    await callback.answer('Главное меню')
    await callback.message.edit_text(f"Выберите одно из доступных действий",
                                     reply_markup=kb.main)


@router.callback_query(F.data.startswith('mailbox_'))
async def mailbox_actions(callback: CallbackQuery, mailbox_id=None):
    await callback.answer('Вы выбрали почтовый ящик')
    mailbox_id = mailbox_id if mailbox_id else int(callback.data.split('_')[1])
    await callback.message.edit_text(f"Выберите действие",
                                     reply_markup=await kb.mailbox_menu(mailbox_id))


@router.callback_query(F.data.startswith('check_mailbox_'))
async def check_mailbox(callback: CallbackQuery):
    await callback.answer('Проверка соединения с сервером')
    mailbox_id = int(callback.data.split('_')[2])
    mailbox = await rq.get_mailboxes_by_id(mailbox_id)
    try:
        text = ("Подключено"
                if await mb.Mail(email=mailbox.email, password=mailbox.password).is_connect()
                else "Не удалось подключиться. Проверьте настройки почтового ящика (правильный логин и пароль, "
                     "разрешение в настройках почтового ящика для работы с IMAP).\n"
                     "Настройки почты Yandex - https://yandex.ru/support/mail/mail-clients/others.html\n"
                     "Настройки почты Mail - https://help.mail.ru/mail/mailer/popsmtp")
        await callback.message.edit_text(text=text, reply_markup=await kb.mailbox_checking(mailbox_id),
                                         disable_web_page_preview=True)
    except ValueError as e:
        await callback.message.edit_text(text=str(e), reply_markup=await kb.mailbox_checking(mailbox_id))


@router.callback_query(F.data.startswith('delete_mailbox_'))
async def delete_mailbox(callback: CallbackQuery):
    mailbox_id = int(callback.data.split('_')[2])
    await rq.delete_mailbox_by_id(mailbox_id)
    await callback.answer('Почтовый ящик удален')
    await checking_mailboxes(callback)


@router.callback_query(F.data.startswith('create_rule_'))
async def create_rule(callback: CallbackQuery, state: FSMContext):
    mailbox_id = int(callback.data.split('_')[2])
    await state.update_data(mailbox_id=mailbox_id)
    await callback.answer('Введите адрес электронной почты с которой необходимо отслеживать письма')
    await state.set_state(RegRule.email)
    await callback.message.edit_text('Введите адрес с которой необходимо отслеживать письма:')


@router.message(RegRule.email)
async def enter_email(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    await message.answer("Выберите действия с входящими сообщениями:", reply_markup=kb.action)


@router.callback_query(F.data.startswith('track_'))
async def get_action(callback: CallbackQuery, state: FSMContext):
    action = callback.data.split('_')[1]
    await callback.answer('Введите адрес электронной почты с которой необходимо отслеживать письма')
    await state.update_data(action=action)
    data = await state.get_data()
    await rq.set_rule(mailbox_id=data['mailbox_id'], email=data['email'], action=data['action'])
    await mailbox_actions(callback, int(data['mailbox_id']))
    await state.clear()


@router.callback_query(F.data.startswith('rules_list_'))
async def show_rules(callback: CallbackQuery, mailbox_id=None):
    mailbox_id = mailbox_id if mailbox_id else int(callback.data.split('_')[2])
    await callback.answer('Список правил для почтового ящика')
    await callback.message.edit_text('Список правил для почтового ящика',
                                     reply_markup=await kb.inline_rules(mailbox_id))


@router.callback_query(F.data.startswith('rule_'))
async def rule(callback: CallbackQuery):
    rule_id = int(callback.data.split('_')[1])
    await callback.answer('Выберите действие для правила')
    await callback.message.edit_text('Выберите действие',
                                     reply_markup=await kb.rule_menu(rule_id=rule_id))


@router.callback_query(F.data.startswith('delete_rule_'))
async def delete_rule(callback: CallbackQuery):
    rule_id = int(callback.data.split('_')[2])
    await rq.delete_rule_by_id(rule_id=rule_id)
    mailbox_id = int(callback.data.split('_')[3])
    await callback.answer('Правило удалено')
    await show_rules(callback, mailbox_id)
