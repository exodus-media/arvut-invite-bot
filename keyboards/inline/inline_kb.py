from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)


inline_btn_1 = InlineKeyboardButton('Первая кнопка!', callback_data='button1')
inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1)

# Отдадим пользователю клавиатуру с выбором языков
languages_markup = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(text="Русский", callback_data="lang_ru"),
            InlineKeyboardButton(text="English", callback_data="lang_en"),
            InlineKeyboardButton(text="Српски", callback_data="lang_sr")
        ]
    ]
)