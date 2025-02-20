from aiogram.dispatcher.filters.state import State, StatesGroup


class UserStates(StatesGroup):
    get_voice_name = State()
    get_voice = State()


class AdminStates(StatesGroup):
    edit_prevoice = State()
    edit_prevoice_title = State()
    edit_prevoice_tag = State()
    