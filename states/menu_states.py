from aiogram.dispatcher.filters.state import State, StatesGroup


# States
class Start(StatesGroup):
    lang_menu = State()
    approve_invite = State()


class Menu(StatesGroup):
    global_menu = State()
    main_list_menu = State()
    list_menu = State()
    check_list_menu = State()
    proof_delete_user = State()

    black_list_menu = State()
    check_black_list_menu = State()
    proof_delete_black_user = State()

    request_menu = State()
    approve_request = State()
    repeat_send_approve_request = State()
    profile_menu = State()

    select_language = State()


class AboutMe(StatesGroup):
    check_input = State()
    check_input_login = State()
    check_input_password = State()


class Admin(StatesGroup):
    main_menu = State()
    send_menu = State()
    check_send_menu = State()


