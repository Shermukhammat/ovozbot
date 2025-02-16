from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from loader import db



class Keyboards:

    user_home_menu = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton("Kulgili ovozlar 😆"), KeyboardButton("Tabriklar 🎉")],
        [KeyboardButton("She'rlar 📚"), KeyboardButton("🏆 Top ovozlar")],
        [KeyboardButton("🎤 Ovoz qo'shish ➕")]
    ], resize_keyboard=True, is_persistent = True)

    buttons = [[KeyboardButton(list(button.keys())[0]) for button in row] for row in db.QIZQARLI_OVOZLAR]
    buttons.append([KeyboardButton("⬅️ Orqaga")])
    kulgili_ovozlar = ReplyKeyboardMarkup(buttons.copy(), resize_keyboard = True, one_time_keyboard = False, is_persistent=True)

    buttons = [[KeyboardButton(list(button.keys())[0]) for button in row] for row in db.SHERLAR]
    buttons.append([KeyboardButton("⬅️ Orqaga")])
    sherlar = ReplyKeyboardMarkup(buttons.copy(), resize_keyboard = True, one_time_keyboard=False, is_persistent=True)

    buttons = [[KeyboardButton(list(button.keys())[0]) for button in row] for row in db.TABRIKLAR]
    buttons.append([KeyboardButton("⬅️ Orqaga")])
    tabriklar = ReplyKeyboardMarkup(buttons.copy(), resize_keyboard = True, one_time_keyboard=False, is_persistent=True)