from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database import requests as rq

main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Зарегистрировать почтовый ящик", callback_data='registration')],
    [InlineKeyboardButton(text="Список почтовых ящиков", callback_data='checking_mailboxes')]
])


async def web_app_kb(html_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Открыть письмо", web_app=WebAppInfo(url=f'https://127.0.0.1:5000/{html_id}'))]
        ])


action = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Отслеживать всю информацию из писем", callback_data='track_all')],
    [InlineKeyboardButton(text="Отслеживать файлы из писем", callback_data='track_file')],
    [InlineKeyboardButton(text="Отслеживать текст из писем", callback_data='track_text')]
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
        [InlineKeyboardButton(text="📩 Создать правило для получения писем", callback_data=f'create_rule_{mailbox_id}')],
        [InlineKeyboardButton(text="📄 Список правил для почты", callback_data=f'rules_list_{mailbox_id}')],
        [InlineKeyboardButton(text="🌐 Проверить соединение с сервером",
                              callback_data=f'check_mailbox_{mailbox_id}')],
        [InlineKeyboardButton(text="❌ Удалить почтовый ящик", callback_data=f'delete_mailbox_{mailbox_id}')],
        [InlineKeyboardButton(text="🔙 Назад", callback_data='checking_mailboxes'),
         InlineKeyboardButton(text="🔝 Начало", callback_data='start')]
    ])


async def mailbox_checking(mailbox_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data=f'mailbox_{mailbox_id}'),
         InlineKeyboardButton(text="🔝 Начало", callback_data='start')]
    ])


async def inline_rules(mailbox_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    rules = await rq.get_rules(mailbox_id)
    action_text = {'all': 'все содержимое письма', 'file': 'только файлы', 'text': 'только текст'}
    for rule in rules:
        keyboard.add(InlineKeyboardButton(text=f'Получать {action_text[rule.action]} от "{rule.email}"',
                                          callback_data=f'rule_{rule.rule_id}'))
    keyboard.add(InlineKeyboardButton(text='⬅️ Назад', callback_data=f'mailbox_{mailbox_id}'))
    return keyboard.adjust(1).as_markup()


async def rule_menu(rule_id: int) -> InlineKeyboardMarkup:
    mailbox_id = await rq.get_mailbox_id_by_rule(rule_id=rule_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Удалить правило", callback_data=f'delete_rule_{rule_id}_{mailbox_id}')],
        [InlineKeyboardButton(text="🔙 Назад", callback_data=f'rules_list_{mailbox_id}'),
         InlineKeyboardButton(text="🔝 Начало", callback_data='start')]
    ])

main_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🔝 Начало", callback_data='start')]
])
