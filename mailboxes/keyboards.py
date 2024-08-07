from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo


async def web_app_kb(html_id: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Открыть письмо",
                              web_app=WebAppInfo(url=f'https://flask-brovko-sergey.amvera.io/{html_id}'))]
        ])
