from aiogram.dispatcher.filters.state import State, StatesGroup


class UserStates(StatesGroup):
    get_voice_name = State()
    get_voice = State()


class AddVoice(StatesGroup):
    get_title = State()
    get_tag = State()
    get_file = State()

class AdminStates(StatesGroup):
    edit_prevoice = State()
    edit_prevoice_title = State()
    edit_prevoice_tag = State()

    delete_voice = State()
    edit_voice = State()
    edit_voice_title = State()
    edit_voice_tag = State()
    edit_voice_file = State()

    