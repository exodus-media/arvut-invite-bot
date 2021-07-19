from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from loader import _


async def markup_general_menu(lang=None):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)

    if lang:
        btn1 = _('Список', locale=lang)
        btn2 = _('Сгенерировать ссылку', locale=lang)
        btn3 = _('Настройки', locale=lang)
        btn4 = 'SOS/INFO'
        btn5 = 'FAQ'

    else:
        btn1 = _('Список')
        btn2 = _('Сгенерировать ссылку')
        btn3 = _('Настройки')
        btn4 = 'SOS/INFO'
        btn5 = 'FAQ'

    markup.row(btn1, btn2)
    markup.row(btn3, btn5)
    markup.row(btn4)

    return markup


async def socium_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    btn1 = _('Граф сети')
    btn2 = _('Показать список')
    btn3 = _('Черный список')
    btn4 = _('Назад')

    markup.row(btn1, btn2)
    markup.row(btn3, btn4)

    return markup


async def back_kb():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    btn1 = _('Назад')
    markup.row(btn1)

    return markup


async def yes_or_no(lang=None):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)

    if lang:
        btn1 = _('Да', locale=lang)
        btn2 = _('Нет', locale=lang)
    else:
        btn1 = _('Да', locale=lang)
        btn2 = _('Нет', locale=lang)

    markup.row(btn1, btn2)
    return markup


async def markup_profile_menu(lang=None):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)

    if lang:
        btn1 = _("Личный кабинет", locale=lang)
        btn2 = _('Язык', locale=lang)
        btn3 = _("Меню", locale=lang)

    else:
        btn1 = _("Личный кабинет")
        btn2 = _('Язык')
        btn3 = _("Меню")

    markup.add(btn1, btn2, btn3)

    return markup


async def markup_select_lang():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)

    btn1 = "Русский"
    btn2 = "English"
    btn3 = "Srpski"
    btn4 = _("Назад")

    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    return markup


async def markup_edit_profile():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)

    btn1 = _("Изменить логин")
    btn2 = _("Изменить пароль")
    btn3 = _("Назад")

    markup.add(btn1, btn2, btn3)
    return markup


async def network_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    btn1 = _('Назад')
    btn2 = _('Отменить связь')
    markup.row(btn1, btn2)

    return markup


async def black_network_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    btn1 = _('Назад')
    btn2 = _('Восстановить связь')
    markup.row(btn1, btn2)

    return markup


async def markup_admin_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)

    btn2 = _("Отправить уведомление")
    btn3 = _("Меню")

    markup.add(btn2, btn3)
    return markup


async def markup_send_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)

    btn1 = _("Да")
    btn2 = _("Нет")
    btn3 = _("Меню")

    markup.add(btn1, btn2, btn3)
    return markup
