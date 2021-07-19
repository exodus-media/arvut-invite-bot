import asyncio
import os

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import CallbackQuery
import networkx as nx
import matplotlib.pyplot as plt
from validate_email import validate_email

from data.config import LOCALES_DIR
from keyboards.default.menu import markup_general_menu, back_kb, yes_or_no, markup_profile_menu, markup_edit_profile, \
    network_menu, black_network_menu, markup_admin_menu, markup_send_menu, socium_menu, markup_select_lang
from keyboards.inline.inline_kb import languages_markup
from loader import dp, bot, _
from states.menu_states import Menu, Start, AboutMe, Admin
from utils.db_api.postgresql import db
from utils.functions import is_digit, text_sum_digit, check_number_dict, AESCipher
from utils.message_text import text_help_menu_func_ru, text_help_about_menu_ru, text_help_menu_func_en, \
    text_help_about_menu_en, text_help_about_menu_sr, text_help_menu_func_sr
from utils.graph_search import bfs, shortest_path
from utils.util_bot import send_message


async def make_hash(text):
    hash = text.encode().hex()
    return hash


async def ref_info(text):
    bytes_object = bytes.fromhex(text)
    text = bytes_object.decode("ASCII")
    return text


async def create_link(from_id):
    bot_username = (await bot.me).username
    ref = str(from_id)
    hash = await make_hash(ref)
    link = f"https://t.me/{bot_username}?start={hash}"
    return link


async def create_graph_list_for_message(user_id, you_id):
    all_users = await db.select_all_users()
    dict_graph = dict()
    for user_ in all_users:
        dict_graph[user_['id']] = user_['my_list']
    list_users_id = set(bfs(dict_graph, user_id))
    list_users_id.discard(user_id)
    list_users_id.discard(you_id)


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message, state: FSMContext):
    await bot.delete_message(message.chat.id, message.message_id)

    user_id = message.chat.id
    old_user = await db.select_user_one(id=user_id)

    referral = message.get_args()

    if old_user:
        if referral:
            referral = await ref_info(referral)
            from_id = int(referral)
            user_from = await db.select_user_one(id=from_id)
            await state.update_data(referral_id=from_id)

            text_send = _('Вы хотите принять приглашение от {}').format(user_from["name"])
            markup = await yes_or_no()
            await Start.approve_invite.set()
            await send_message(user_id, text_send, reply_markup=markup)
        else:
            markup = await markup_general_menu()
            await Menu.global_menu.set()
            await send_message(user_id, _('Меню'), reply_markup=markup)
            return
    else:
        await Start.lang_menu.set()
        await state.update_data(referral=referral)
        await send_message(user_id,
                           "Приветствуем вас в Арвут Ададит Бот!\nВыберите язык.\n\nWelcome to Arvut Addadid Bot "
                           "Bot!\nSelect a language.\n\nДобродошли у Арвут Ададит Бот!\nИзаберите језик.",
                           reply_markup=languages_markup)


@dp.message_handler(text='FAQ', state=Menu.global_menu)
async def bot_start(message: types.Message, state: FSMContext):
    await bot.delete_message(message.chat.id, message.message_id)
    user_id = message.chat.id
    user_me = await db.select_user_one(id=user_id)
    lang = user_me['language']

    if lang == 'ru':
        text_faq = await text_help_menu_func_ru()
        text_faq_about_menu = await text_help_about_menu_ru()
    elif lang == 'en':
        text_faq = await text_help_menu_func_en()
        text_faq_about_menu = await text_help_about_menu_en()
    elif lang == 'sr':
        text_faq = await text_help_menu_func_sr()
        text_faq_about_menu = await text_help_about_menu_sr()

    await send_message(user_id, text_faq)
    await send_message(user_id, text_faq_about_menu)


@dp.callback_query_handler(text_contains="lang", state=Start.lang_menu)
async def change_language(call: CallbackQuery, state: FSMContext):
    # Достаем последние 2 символа (например ru)
    lang = call.data[-2:]

    data = await state.get_data()
    referral = data['referral']
    user = call.from_user
    user_id = user.id

    await send_message(user_id, _("Вы выбрали русский язык", locale=lang))

    await db.add_user(id=user_id,
                      name=user.full_name,
                      language=lang)

    if referral:
        referral = await ref_info(referral)
        from_id = int(referral)
        user_from = await db.select_user_one(id=from_id)
        await state.update_data(referral_id=from_id)

        text_send = _('Вы хотите принять приглашение от {}', locale=lang).format(user_from["name"])
        markup = await yes_or_no(lang=lang)
        await Start.approve_invite.set()
        await send_message(user_id, text_send, reply_markup=markup)
    else:
        markup = await markup_general_menu(lang=lang)
        await send_message(user_id,
                           _('Вы зарегестрированы. Здесь вы можете начать собирать свою сеть', locale=lang),
                           reply_markup=markup)

        await Menu.global_menu.set()
        # После того, как мы поменяли язык, в этой функции все еще указан старый, поэтому передаем locale=lang
        await send_message(user_id, _('Меню', locale=lang), reply_markup=markup)


@dp.message_handler(state=Start.approve_invite)
async def approve_invite(message: types.Message, state: FSMContext):
    await bot.delete_message(message.chat.id, message.message_id)

    in_text = message.text
    user_id = message.chat.id

    markup = await markup_general_menu()
    await Menu.global_menu.set()

    if _('Да') in in_text:
        data = await state.get_data()
        referral_id = data['referral_id']
        user_from = await db.select_user_one(id=referral_id)

        list_refferal = user_from['my_list']
        if user_id in list_refferal:
            await send_message(user_id, _('Вы уже подтвердил прямую договоренность с участником'), reply_markup=markup)
            return

        if user_id == user_from['id']:
            await send_message(user_id, _('Вы нажали на свою ссылку'), reply_markup=markup)
            return

        user_me = await db.select_user_one(id=user_id)
        # добавляем в мой основной список
        my_list_to_me = user_me['my_list']
        my_list_to_me.append(referral_id)
        await db.update_user(id=user_id,
                             update_field='my_list',
                             update_value=my_list_to_me)

        # добавляем в его основной список
        list_refferal.append(user_id)
        await db.update_user(id=referral_id,
                             update_field='my_list',
                             update_value=list_refferal)

        await send_message(referral_id, _('{} подтвердил прямую договоренность с вами').format(user_me['name']))

        text_message = _('Вы подтвердили прямую договоренность с {}\n').format(user_from['name'])
        markup = await markup_general_menu()
        await Menu.global_menu.set()
        await send_message(user_id, text_message, reply_markup=markup)

    await send_message(user_id, _('Меню'), reply_markup=markup)


@dp.message_handler(lambda message: _('Сгенерировать ссылку') in message.text, state=Menu.global_menu)
async def create_ref(message: types.Message, state: FSMContext):
    await bot.delete_message(message.chat.id, message.message_id)

    user_id = message.chat.id

    link = await create_link(user_id)
    text = _('Ваша ссылка для приглашения в список:\n') + link
    await send_message(user_id, text)


'''
Меню со списком сети и его просмотром
'''


async def circle_list_base(message: types.Message, state: FSMContext):
    user_id = message.chat.id
    user_me = await db.select_user_one(id=user_id)
    count = 0

    my_black_list = user_me['black_list']
    text_message = _('\n<b>Подтвержденные лично:</b>\n')
    list_users_me_id = user_me['my_list']
    dict_my_invite = {}
    for you_id in list_users_me_id:
        if you_id in my_black_list:
            continue
        count += 1
        user_you = await db.select_user_one(id=you_id)
        text_link_user = f'<a href="tg://user?id={user_you["id"]}">{user_you["name"]}</a>'
        text_message += f'{count}. {text_link_user}\n'
        dict_my_invite[count] = you_id

    text_message += _('\n<b>Полный список:</b>\n')
    dict_all_socium = {}
    all_users = await db.select_all_users()
    dict_graph = dict()
    for user_ in all_users:
        dict_graph[user_['id']] = user_['my_list']
    list_users_all = bfs(dict_graph, user_id)

    list_users_all = set(list_users_all)
    list_users_all.discard(user_id)

    if len(list_users_all) != 0:
        for id_ in list_users_all:
            if id_ in list_users_me_id:
                continue
            if id_ in my_black_list:
                continue

            count += 1

            user_ = await db.select_user_one(id=id_)
            text_link_user = f'<a href="tg://user?id={user_["id"]}">{user_["name"]}</a>'
            text_message += f"{count}. {text_link_user}\n"
            dict_all_socium[count] = id_

    text_message += _('\n<b>Введите номер участника для выбора действий:</b>')

    await Menu.list_menu.set()
    await state.update_data(dict_my_invite=dict_my_invite, dict_all_socium=dict_all_socium)

    markup = await back_kb()

    await send_message(user_id, text_message, reply_markup=markup)


@dp.message_handler(lambda message: _("Список") in message.text, state=Menu.global_menu)
async def main_list_menu(message: types.Message, state: FSMContext):
    await bot.delete_message(message.chat.id, message.message_id)
    user_id = message.chat.id
    user_me = await db.select_user_one(id=user_id)

    count = 0
    all_users = await db.select_all_users()
    dict_graph = dict()
    for user_ in all_users:
        dict_graph[user_['id']] = user_['my_list']
    list_users_all = bfs(dict_graph, user_id)

    list_users_all = set(list_users_all)
    list_users_all.discard(user_id)

    my_black_list = user_me['black_list']
    list_users_me_id = user_me['my_list']
    for you_id in list_users_me_id:
        if you_id in my_black_list:
            continue
        count += 1

    if len(list_users_all) != 0:
        for id_ in list_users_all:
            if id_ in list_users_me_id:
                continue
            if id_ in my_black_list:
                continue

            count += 1

    old_count_pool = user_me['count_pool']
    now_count_pool = count
    text_pool = _('Предыдущий размер пула = {}€\nТекущий размер пула = {}€\n').format(old_count_pool * 100,
                                                                                      now_count_pool * 100)
    if now_count_pool > old_count_pool:
        text_pool += _('Прирост {}€\n').format((now_count_pool - old_count_pool) * 100)
    elif now_count_pool < old_count_pool:
        text_pool += _('Убыль {}€\n').format((now_count_pool - old_count_pool) * 100)

    await db.update_user(id=user_id,
                         update_field='count_pool',
                         update_value=now_count_pool)

    markup = await socium_menu()
    await Menu.main_list_menu.set()
    await send_message(user_id, text_pool, reply_markup=markup)


@dp.message_handler(state=Menu.main_list_menu)
async def circle_list(message: types.Message, state: FSMContext):
    await bot.delete_message(message.chat.id, message.message_id)
    in_text = message.text
    user_id = message.chat.id

    if _('Назад') in in_text:
        markup = await markup_general_menu()
        await Menu.global_menu.set()
        await send_message(user_id, _('Меню'), reply_markup=markup)
        return

    elif _('Показать') in in_text:
        await circle_list_base(message, state)
        return

    elif _('Граф') in in_text:
        await graph(message)
        return

    elif _('Черный') in in_text:
        await black_list_show(message, state)
        return

    else:
        text = await check_number_dict()
        await send_message(message.chat.id, text)
        return


@dp.message_handler(state=Menu.list_menu)
async def circle_list(message: types.Message, state: FSMContext):
    await bot.delete_message(message.chat.id, message.message_id)

    in_text = message.text
    user_id = message.chat.id

    if _('Назад') in in_text:
        markup = await socium_menu()
        await Menu.main_list_menu.set()
        await send_message(user_id, _('Просмотр списка'), reply_markup=markup)
        return

    if not await is_digit(in_text):
        text = await text_sum_digit()
        await send_message(user_id, text)
        return

    data = await state.get_data()
    dict_my_invite = data["dict_my_invite"]
    dict_all_socium = data["dict_all_socium"]

    if in_text in dict_my_invite:
        you_id = dict_my_invite[in_text]
        user_you = await db.select_user_one(id=you_id)
        user_you_my_list = user_you['my_list']
        await state.update_data(you_id=you_id)

        text_message = _('{} связан с вами лично').format(user_you['name'])
        count = 0
        if user_you_my_list:
            text_message += _('\n\nПодтвержденные лично {}:\n').format(user_you['name'])
            for id_ in user_you_my_list:
                count += 1
                user_ = await db.select_user_one(id=id_)
                text_link_user = f'<a href="tg://user?id={user_["id"]}">{user_["name"]}</a>'
                text_message += f"{count}. {text_link_user}\n"

        await Menu.check_list_menu.set()
        markup = await network_menu()
        await send_message(user_id, text_message, reply_markup=markup)
        return

    elif in_text in dict_all_socium:
        you_id = dict_all_socium[in_text]
        user_you = await db.select_user_one(id=you_id)
        user_you_my_list = user_you['my_list']

        await state.update_data(you_id=you_id)

        all_users = await db.select_all_users()
        dict_graph = dict()
        for user_ in all_users:
            dict_graph[user_['id']] = user_['my_list']
        route_me_to_user = shortest_path(dict_graph, user_id, you_id)

        text_invite = ' - '.join([(await db.select_user_one(id=i))['name'] for i in route_me_to_user])
        count = 0
        if user_you_my_list:
            text_invite += _('\n\nПодтвержденные лично {}:\n').format(user_you['name'])
            for id_ in user_you_my_list:
                count += 1
                user_ = await db.select_user_one(id=id_)
                text_link_user = f'<a href="tg://user?id={user_["id"]}">{user_["name"]}</a>'
                text_invite += f"{count}. {text_link_user}\n"

        await Menu.check_list_menu.set()
        markup = await network_menu()
        await send_message(user_id, text_invite, reply_markup=markup)
        return
    else:
        text = await check_number_dict()
        markup = await back_kb()
        await send_message(message.chat.id, text, reply_markup=markup)
        return


@dp.message_handler(state=Menu.check_list_menu)
async def check_list_menu(message: types.Message, state: FSMContext):
    await bot.delete_message(message.chat.id, message.message_id)

    in_text = message.text
    user_id = message.chat.id

    if _('Назад') in in_text:
        await circle_list_base(message, state)
        return

    elif _('Отменить') in in_text:
        data = await state.get_data()
        you_id = data["you_id"]
        user_you = await db.select_user_one(id=you_id)

        markup = await yes_or_no()
        await Menu.proof_delete_user.set()
        text_message = _('Вы уверены, что хотите отменить связь с участником {}?').format(user_you['name'])
        await send_message(user_id, text_message, reply_markup=markup)
        return


@dp.message_handler(state=Menu.proof_delete_user)
async def proof_delete_user(message: types.Message, state: FSMContext):
    await bot.delete_message(message.chat.id, message.message_id)

    in_text = message.text
    user_id = message.chat.id

    if _('Да') in in_text:
        data = await state.get_data()
        you_id = data["you_id"]

        user_you = await db.select_user_one(id=you_id)
        user_me = await db.select_user_one(id=user_id)

        text_message_you = _('Участник {} отменил с вами связь').format(user_me['name'])
        await send_message(you_id, text_message_you)

        # add in my black_list
        my_black_list = user_me['black_list']
        my_black_list.append(you_id)
        my_black_list = set(my_black_list)
        await db.update_user(id=user_id,
                             update_field='black_list',
                             update_value=list(my_black_list))

        text_message_me = _('Вы отменили связь с участником {}').format(user_you['name'])
        await send_message(user_id, text_message_me)

        # рассылка уведомлений всему списку
        list_users_id = await create_graph_list_for_message(user_id, you_id)

        text_for_all = _('Участник {} прекратил связь с участником {}').format(user_me['name'], user_you['name'])
        for id_ in list_users_id:
            await send_message(id_, text_for_all)
            await asyncio.sleep(0.05)

    markup = await markup_general_menu()
    await Menu.global_menu.set()
    await send_message(user_id, _('Меню'), reply_markup=markup)
    return


'''
Меню с черным списком юзера
'''


# @dp.message_handler(lambda message: 'Black' in message.text, state=Menu.global_menu)
async def black_list_show(message: types.Message, state: FSMContext):
    user_id = message.chat.id
    user_me = await db.select_user_one(id=user_id)
    count = 0

    my_black_list = user_me['black_list']
    dict_my_black_list = {}
    text_message = _('\n<b>Заблокированные мной:</b>\n')

    for you_id in my_black_list:
        count += 1
        user_you = await db.select_user_one(id=you_id)
        text_link_user = f'<a href="tg://user?id={user_you["id"]}">{user_you["name"]}</a>'
        text_message += f'{count}. {text_link_user}\n'
        dict_my_black_list[count] = you_id

    text_message += _('\n<b>Введите номер участника для выбора действий:</b>')

    await Menu.black_list_menu.set()
    await state.update_data(dict_my_black_list=dict_my_black_list)

    markup = await back_kb()
    await send_message(user_id, text_message, reply_markup=markup)


@dp.message_handler(state=Menu.black_list_menu)
async def black_circle_list(message: types.Message, state: FSMContext):
    await bot.delete_message(message.chat.id, message.message_id)

    in_text = message.text
    user_id = message.chat.id

    if _('Назад') in in_text:
        markup = await socium_menu()
        await Menu.main_list_menu.set()
        await send_message(user_id, _('Просмотр списка'), reply_markup=markup)
        return

    if not await is_digit(in_text):
        text = await text_sum_digit()
        await send_message(user_id, text)
        return

    data = await state.get_data()
    dict_my_black_list = data["dict_my_black_list"]

    if in_text in dict_my_black_list:
        you_id = dict_my_black_list[in_text]
        user_you = await db.select_user_one(id=you_id)
        await state.update_data(you_id=you_id)

        text_message = _('Вы разорвали с {} связь').format(user_you['name'])

        await Menu.check_black_list_menu.set()
        markup = await black_network_menu()
        await send_message(user_id, text_message, reply_markup=markup)
        return

    else:
        text = await check_number_dict()
        markup = await back_kb()
        await send_message(message.chat.id, text, reply_markup=markup)
        return


@dp.message_handler(state=Menu.check_black_list_menu)
async def check_black_list_menu(message: types.Message, state: FSMContext):
    await bot.delete_message(message.chat.id, message.message_id)

    in_text = message.text
    user_id = message.chat.id

    if _('Назад') in in_text:
        markup = await markup_general_menu()
        await Menu.global_menu.set()
        await send_message(user_id, _('Меню'), reply_markup=markup)
        return

    elif _('Восстановить') in in_text:
        data = await state.get_data()
        you_id = data["you_id"]
        user_you = await db.select_user_one(id=you_id)

        markup = await yes_or_no()
        await Menu.proof_delete_black_user.set()
        text_message = _('Вы уверены, что хотите восстановить связь с участником {}?').format(user_you['name'])
        await send_message(user_id, text_message, reply_markup=markup)
        return


@dp.message_handler(state=Menu.proof_delete_black_user)
async def proof_delete_black_user(message: types.Message, state: FSMContext):
    await bot.delete_message(message.chat.id, message.message_id)

    in_text = message.text
    user_id = message.chat.id

    if _('Да') in in_text:
        data = await state.get_data()
        you_id = data["you_id"]

        user_you = await db.select_user_one(id=you_id)
        user_me = await db.select_user_one(id=user_id)

        text_message_you = _('Участник {} восстановил с вами связь').format(user_me['name'])
        await send_message(you_id, text_message_you)

        # delete from my black_list
        my_black_list = set(user_me['black_list'])
        my_black_list.discard(you_id)
        await db.update_user(id=user_id,
                             update_field='black_list',
                             update_value=list(my_black_list))

        text_message_me = _('Вы восстановили связь с участником {}').format(user_you['name'])
        await send_message(user_id, text_message_me)

        # рассылка уведомлений всему списку
        list_users_id = await create_graph_list_for_message(user_id, you_id)
        text_for_all = _('Участник {} восстановил связь с участником {}').format(user_me['name'], user_you['name'])
        for id_ in list_users_id:
            await send_message(id_, text_for_all)
            await asyncio.sleep(0.05)

    markup = await markup_general_menu()
    await Menu.global_menu.set()
    await send_message(user_id, _('Меню'), reply_markup=markup)
    return


'''
Меню с настройками юзера
'''


@dp.message_handler(lambda message: _("Настройки") in message.text, state=Menu.global_menu)
async def profile_handler(message: types.Message):
    await bot.delete_message(message.chat.id, message.message_id)
    user_id = message.chat.id

    await Menu.profile_menu.set()
    markup = await markup_profile_menu()

    await send_message(user_id, _('Настройки'), reply_markup=markup, disable_web_page_preview=True)


async def edit_lang_user(message: types.Message, lang):
    await db.update_user(message.chat.id, 'language', lang)

    await Menu.profile_menu.set()
    markup = await markup_profile_menu(lang)
    await send_message(message.chat.id, _("Ваш язык был изменен на Русский", locale=lang), reply_markup=markup)


async def about_me_settings(message, user_):
    await AboutMe.check_input.set()
    markup = await markup_edit_profile()
    if user_['login']:
        login = user_['login']
    else:
        login = _('не задан')

    if user_['password']:
        password = user_['password']
        aes_cipher = await AESCipher.create(LOCALES_DIR)
        password = await aes_cipher.decrypt(password)
    else:
        password = _('не задан')

    bot_text = _('Логин пользователя: {}\n').format(login)
    bot_text += _('Пароль пользователя: {}').format(password)
    await send_message(message.chat.id, bot_text, reply_markup=markup)


@dp.message_handler(state=Menu.profile_menu)
async def profile_menu_check(message: types.Message, state: FSMContext):
    in_text = message.text
    await bot.delete_message(message.chat.id, message.message_id)

    user_id = message.chat.id
    user_me = await db.select_user_one(id=user_id)

    if _("Личный") in in_text:
        await about_me_settings(message, user_me)

    elif _("Язык") in in_text:
        markup = await markup_select_lang()
        await Menu.select_language.set()
        await send_message(user_id, _('Выберете язык'), reply_markup=markup)

    elif _('Меню') in in_text:
        markup = await markup_general_menu()
        await Menu.global_menu.set()
        await send_message(user_id, _('Меню'), reply_markup=markup)

    return


@dp.message_handler(state=Menu.select_language)
async def about_me_check_input(message: types.Message):
    in_text = message.text
    await bot.delete_message(message.chat.id, message.message_id)

    if "Рус" in in_text:
        await edit_lang_user(message, 'ru')

    elif "Engl" in in_text:
        await edit_lang_user(message, 'en')

    elif 'Srp' in in_text:
        await edit_lang_user(message, 'sr')

    elif _('Назад') in in_text:
        user_id = message.chat.id
        await Menu.profile_menu.set()
        markup = await markup_profile_menu()

        await send_message(user_id, _('Настройки'), reply_markup=markup, disable_web_page_preview=True)


@dp.message_handler(state=AboutMe.check_input)
async def about_me_check_input(message: types.Message):
    in_text = message.text
    await bot.delete_message(message.chat.id, message.message_id)

    user_id = message.chat.id
    user_me = await db.select_user_one(id=user_id)

    if _("Изменить логин") in in_text:
        await AboutMe.check_input_login.set()
        markup = await back_kb()

        if user_me['login']:
            login = user_me['login']
        else:
            login = _('не задан')

        bot_text = _('Текущий логин пользователя: {}\nВведите новый логин в формате email').format(login)
        await send_message(message.chat.id, bot_text, reply_markup=markup)

    elif _("Изменить пароль") in in_text:
        await AboutMe.check_input_password.set()
        markup = await back_kb()
        if user_me['password']:
            password = user_me['password']
            aes_cipher = await AESCipher.create(LOCALES_DIR)
            password = await aes_cipher.decrypt(password)

        else:
            password = _('не задан')

        bot_text = _('Текущий пароль пользователя: {}\n\nВведите пароль, не менее 8 и не более 16 символов').format(password)
        await send_message(message.chat.id, bot_text, reply_markup=markup)
    elif _("Назад") in in_text:
        await Menu.profile_menu.set()
        markup = await markup_profile_menu()
        await send_message(message.chat.id, _("Настройки"), reply_markup=markup)


@dp.message_handler(state=AboutMe.check_input_password)
async def about_me_check(message: types.Message):
    password = message.text
    await bot.delete_message(message.chat.id, message.message_id)

    user_id = message.chat.id
    user_me = await db.select_user_one(id=user_id)

    if _('Назад') in password:
        await about_me_settings(message, user_me)

        return

    if len(password) > 16 or len(password) < 8:
        text = _("Длина пароля должна быть не менее 8 и не более 16 символов!\nПопробуйте снова.")
        await send_message(message.chat.id, text)
        return

    aes_cipher = await AESCipher.create(LOCALES_DIR)
    cipherpass = await aes_cipher.encrypt(password)
    await db.update_user(user_id, 'password', cipherpass)

    await Menu.profile_menu.set()
    markup = await markup_profile_menu()
    bot_text = 'Ваш новый пароль:\n{}'.format(password)
    await send_message(message.chat.id, bot_text, reply_markup=markup)


@dp.message_handler(state=AboutMe.check_input_login)
async def edit_my_name_check(message: types.Message):
    in_text = message.text
    await bot.delete_message(message.chat.id, message.message_id)

    user_id = message.chat.id
    user_me = await db.select_user_one(id=user_id)

    if _('Назад') in in_text:
        await about_me_settings(message, user_me)
        return

    is_valid = validate_email(in_text)
    if not is_valid:
        text = _("Логин должен быть в формате email!\nПопробуйте снова.")
        await send_message(message.chat.id, text)
        return

    await db.update_user(user_id, 'login', in_text)

    await Menu.profile_menu.set()
    markup = await markup_profile_menu()
    bot_text = 'Ваш новый логин\n{}'.format(in_text)
    await send_message(message.chat.id, bot_text, reply_markup=markup)


# @dp.message_handler(commands=['graph'], state=Menu.global_menu)
# @dp.message_handler(lambda message: 'Graph' in message.text, state=Menu.global_menu)
async def graph(message: types.Message):
    user_id = message.chat.id

    all_users = await db.select_all_users()
    dict_graph = dict()
    for user_ in all_users:
        dict_graph[user_['id']] = user_['my_list']
    list_users_id = bfs(dict_graph, user_id)
    count_people = len(list_users_id)
    list_users_all = [await db.select_user_one(id=id_) for id_ in list_users_id]
    list_graph = [(user_['name'], (await db.select_user_one(id=id_))['name']) for user_ in list_users_all for id_
                  in list_users_id if id_ not in user_['black_list']]
    count_lines = len(list_graph)

    black_list_graph = [(user_['name'], (await db.select_user_one(id=id_))['name']) for user_ in list_users_all for id_
                        in user_['black_list']]
    for list_black in black_list_graph:
        try:
            list_graph.remove(list_black)
        except:
            continue
    black_list_graph_reverse = [list_black[-1::-1] for list_black in black_list_graph]
    for list_black in black_list_graph_reverse:
        try:
            list_graph.remove(list_black)
        except:
            continue

    G = nx.DiGraph()
    G.add_edges_from(list_graph)

    # Specify the edges you want here
    my_user = await db.select_user_one(id=user_id)
    my_user_list = my_user['my_list']
    red_edges = [(my_user['name'], (await db.select_user_one(id=id_))['name']) for id_ in my_user_list]
    val_map_red = {edge[1]: 1.0 for edge in red_edges}
    val_map_red[red_edges[0][0]] = 1.0
    values = [val_map_red.get(node, 0.5714285714285714) for node in G.nodes()]

    for list_black in black_list_graph:
        try:
            red_edges.remove(list_black)
        except:
            continue

    black_edges = [edge for edge in G.edges() if edge not in red_edges]

    # Need to create a layout when doing
    # separate calls to draw nodes and edges
    pos = nx.shell_layout(G)
    nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'), node_color=values, node_size=300)
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edges(G, pos, edgelist=red_edges, edge_color='r', arrows=True)
    nx.draw_networkx_edges(G, pos, edgelist=black_edges, arrows=False)

    plt.savefig('./data/graph.jpg', bbox_inches='tight')
    plt.close()
    with open(os.path.join('./data', 'graph.jpg'), 'rb') as file:
        await bot.send_photo(message.chat.id, file, disable_notification=True)
    if os.path.isfile('./data/graph.jpg'):
        os.remove('./data/graph.jpg')

    text_for_graph = '{} peoples, {} lines'.format(count_people, count_lines)
    await send_message(message.chat.id, text_for_graph)


'''
Меню с отправкой срочного сообщения в мою сеть
'''


async def admin_view(message):
    user_id = message.chat.id
    user_me = await db.select_user_one(id=user_id)

    text = _("Количество участников в моей сети: {}").format(user_me['count_pool'])

    await Admin.main_menu.set()
    markup = await markup_admin_menu()
    await send_message(message.chat.id, text, reply_markup=markup)


@dp.message_handler(lambda message: 'SOS' in message.text, state=Menu.global_menu)
async def admin_handler(message: types.Message):
    await bot.delete_message(message.chat.id, message.message_id)

    await admin_view(message)


@dp.message_handler(state=Admin.main_menu)
async def admin_main_menu(message: types.Message):
    in_text = message.text
    user_id = message.chat.id

    await bot.delete_message(user_id, message.message_id)

    if _("Отправить") in in_text:
        text = _("Введите текст для отправки пользователям")
        markup = types.ReplyKeyboardRemove()
        await send_message(user_id, text, reply_markup=markup)
        await Admin.send_menu.set()
        return
    elif _("Меню") in in_text:
        markup = await markup_general_menu()
        await Menu.global_menu.set()
        await send_message(user_id, _('Меню'), reply_markup=markup)
        return


@dp.message_handler(state=Admin.send_menu)
async def admin_send_menu(message: types.Message, state: FSMContext):
    in_text = message.text
    user_id = message.chat.id

    await bot.delete_message(message.chat.id, message.message_id)

    text = _("Вы ввели текст для отправки:\n<b>{}</b>").format(in_text)
    await send_message(user_id, text)

    markup = await markup_send_menu()
    await Admin.check_send_menu.set()
    await state.update_data(admin_text=in_text)

    await bot.send_message(user_id, _('Подтвердите отправку'), reply_markup=markup)


@dp.message_handler(state=Admin.check_send_menu)
async def admin_check_send_menu(message: types.Message, state: FSMContext):
    in_text = message.text
    user_id = message.chat.id

    await bot.delete_message(message.chat.id, message.message_id)

    if _('Да') in in_text:
        user_me = await db.select_user_one(id=user_id)

        # рассылка уведомлений всему списку
        all_users = await db.select_all_users()
        dict_graph = dict()
        for user_ in all_users:
            dict_graph[user_['id']] = user_['my_list']
        list_users_id = set(bfs(dict_graph, user_id))
        list_users_id.discard(user_id)

        text_link_user = f'<a href="tg://user?id={user_me["id"]}">{user_me["name"]}</a>'
        text_start = _('<b>Участник {} нажал экстренную кнопку SOS/INFO с текстом:</b>\n\n').format(text_link_user)
        data_state = await state.get_data()
        text_for_mes = text_start + data_state['admin_text']
        text_for_mes += _('\n\n<b>В сети участника находится {} человек</b>').format(user_me['count_pool'])

        markup = await markup_general_menu()
        await Menu.global_menu.set()
        await send_message(user_id, _("Успешно отправлено"), reply_markup=markup)

        for id_ in list_users_id:
            await send_message(id_, text_for_mes)
            await asyncio.sleep(.05)

        return
    elif _('Нет') in in_text:
        await bot.send_message(user_id, _("Отправка отменена"))
        await admin_view(message)
        return
    elif _('Меню') in in_text:
        markup = await markup_general_menu()
        await Menu.global_menu.set()
        await send_message(user_id, _('Меню'), reply_markup=markup)
        return


'''
Меню со списком заявок и действиями над ними
'''

# @dp.message_handler(lambda message: _('Заявки') in message.text, state=Menu.global_menu)
# async def requests(message: types.Message, state: FSMContext):
#     await bot.delete_message(message.chat.id, message.message_id)
#
#     user_id = message.chat.id
#     count = 1
#
#     my_user = await db.select_user_one(id=user_id)
#     list_to_me = my_user['list_to_me']
#     text_message = _('<b>Входящие:</b>\n')
#     dict_request_to_me = {}
#     for you_id in list_to_me:
#         dict_request_to_me[count] = you_id
#         user_you = await db.select_user_one(id=you_id)
#         text_link_user = f'<a href="tg://user?id={user_you["id"]}">{user_you["name"]}</a>'
#         text_message += f'{count}. {text_link_user}\n'
#         count += 1
#
#     text_message += _('\n<b>Исходящие:</b>\n')
#     list_from_me = my_user['list_from_me']
#     dict_request_from_me = {}
#     for you_id in list_from_me:
#         dict_request_from_me[count] = you_id
#         user_you = await db.select_user_one(id=you_id)
#         text_link_user = f'<a href="tg://user?id={user_you["id"]}">{user_you["name"]}</a>'
#         text_message += f'{count}. {text_link_user}\n'
#         count += 1
#
#     text_message += _('\n<b>Введите номер участника для выбора действий:</b>')
#
#     await Menu.request_menu.set()
#     await state.update_data(dict_request_from_me=dict_request_from_me, dict_request_to_me=dict_request_to_me)
#
#     markup = await back_kb()
#     await send_message(user_id, text_message, reply_markup=markup)
#
#
# @dp.message_handler(state=Menu.request_menu)
# async def request_list(message: types.Message, state: FSMContext):
#     await bot.delete_message(message.chat.id, message.message_id)
#
#     in_text = message.text
#     user_id = message.chat.id
#
#     if _('Назад') in in_text:
#         markup = await markup_general_menu()
#         await Menu.global_menu.set()
#         await send_message(user_id, _('Меню'), reply_markup=markup)
#         return
#
#     if not await is_digit(in_text):
#         text = await text_sum_digit()
#         await send_message(user_id, text)
#         return
#
#     data = await state.get_data()
#     dict_request_from_me = data["dict_request_from_me"]
#     dict_request_to_me = data["dict_request_to_me"]
#
#     if in_text in dict_request_to_me:
#         you_id = dict_request_to_me[in_text]
#         user_you = await db.select_user_one(id=you_id)
#
#         text_message = _(
#             'Вы хотите попасть в сеть {}.\nОтправить повторное уведомление о рассмотрении вашей заявки?').format(
#             user_you['name'])
#         await state.update_data(you_id=you_id)
#
#         markup = await yes_or_no()
#         await Menu.repeat_send_approve_request.set()
#         await send_message(user_id, text_message, reply_markup=markup)
#         return
#
#     elif in_text in dict_request_from_me:
#         you_id = dict_request_from_me[in_text]
#         user_you = await db.select_user_one(id=you_id)
#
#         text_message = _('Пользователь {} просит добавить его в вашу сеть.\nДобавить?').format(user_you['name'])
#         await state.update_data(you_id=you_id)
#
#         markup = await yes_or_no()
#         await Menu.approve_request.set()
#         await send_message(user_id, text_message, reply_markup=markup)
#         return
#
#     else:
#         text = await check_number_dict()
#         await send_message(message.chat.id, text)
#         return
#
#
# @dp.message_handler(state=Menu.repeat_send_approve_request)
# async def repeat_send_approve_request(message: types.Message, state: FSMContext):
#     await bot.delete_message(message.chat.id, message.message_id)
#
#     in_text = message.text
#     user_id = message.chat.id
#
#     if _('Да') in in_text:
#         data = await state.get_data()
#         you_id = data["you_id"]
#         user_you = await db.select_user_one(id=you_id)
#         user_me = await db.select_user_one(id=user_id)
#
#         markup = await markup_general_menu()
#         await Menu.global_menu.set()
#
#         await send_message(you_id, _('Рассмотрите заявку в вашу сеть от участника {}').format(user_me['name']))
#         await send_message(user_id, _('Сообщение на рассмотрение вашей заявки повторно отправлено {}').format(
#             user_you['name']), reply_markup=markup)
#
#     elif _('Нет') in in_text:
#         markup = await markup_general_menu()
#         await Menu.global_menu.set()
#         await send_message(user_id, _('Меню'), reply_markup=markup)
#
#
# @dp.message_handler(state=Menu.approve_request)
# async def request_approve(message: types.Message, state: FSMContext):
#     await bot.delete_message(message.chat.id, message.message_id)
#
#     in_text = message.text
#     user_id = message.chat.id
#
#     if _('Да') in in_text:
#         # обновляем записи у него
#         data = await state.get_data()
#         you_id = data["you_id"]
#         user_you = await db.select_user_one(id=you_id)
#         # удаляем из списка ожидания
#         list_to_me = user_you['list_to_me']
#         list_to_me.remove(user_id)
#         await db.update_user(id=you_id,
#                              update_field='list_to_me',
#                              update_value=list_to_me)
#         # добавляем в его основной список
#         my_list_to_me = user_you['my_list_to_me']
#         my_list_to_me.append(user_id)
#         await db.update_user(id=you_id,
#                              update_field='my_list_to_me',
#                              update_value=my_list_to_me)
#
#         # обновляем записи у меня, удаляя список ожидания
#         user_me = await db.select_user_one(id=user_id)
#         list_from_me = user_me['list_from_me']
#         list_from_me.remove(you_id)
#         await db.update_user(id=user_id,
#                              update_field='list_from_me',
#                              update_value=list_from_me)
#         # добавляем в мой основной список
#         my_list_from_me = user_me['my_list_from_me']
#         my_list_from_me.append(you_id)
#         await db.update_user(id=user_id,
#                              update_field='my_list_from_me',
#                              update_value=my_list_from_me)
#
#         await send_message(you_id, _('{} принял вашу заявку').format(user_me['name']))
#
#         text_message = _('Вы приняли {} в вашу сеть.\n').format(user_you['name'])
#         markup = await markup_general_menu()
#         await Menu.global_menu.set()
#         await send_message(user_id, text_message, reply_markup=markup)
#
#     elif _('Нет') in in_text:
#         markup = await markup_general_menu()
#         await Menu.global_menu.set()
#         await send_message(user_id, _('Меню'), reply_markup=markup)
