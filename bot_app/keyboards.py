from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database import requests as rq

main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Зарегистрировать почтовый ящик", callback_data='registration')],
    [InlineKeyboardButton(text="Список почтовых ящиков", callback_data='checking_mailboxes')]
])


async def inline_mailboxes(chat_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    user_mailboxes = await rq.get_mailboxes(chat_id)
    for mailbox in user_mailboxes:
        keyboard.add(InlineKeyboardButton(text=f'{mailbox.email}', callback_data=f'mailbox_{mailbox.mailbox_id}'))
    keyboard.add(InlineKeyboardButton(text='⬅️ Назад', callback_data='start'))
    return keyboard.adjust(1).as_markup()


async def mailbox_menu(mailbox_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📩 Создать правило для получения писем", callback_data=f'create_{mailbox_id}')],
        [InlineKeyboardButton(text="📄 Список правил для почты", callback_data=f'rules_list_{mailbox_id}')],
        [InlineKeyboardButton(text="🌐 Проверить соединение с сервером",
                              callback_data=f'check_mailbox_{mailbox_id}')],
        [InlineKeyboardButton(text="❌ Удалить почтовый ящик", callback_data=f'delete-mailbox_{mailbox_id}')],
        [InlineKeyboardButton(text="🔙 Назад", callback_data='checking_mailboxes'),
         InlineKeyboardButton(text="🔝 Начало", callback_data='start')]
    ])
