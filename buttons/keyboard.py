from aiogram.types import KeyboardButton, ReplyKeyboardMarkup




class Keyboards:
    user_home_menu = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton("🔍 Ovoz izlash")],
        [KeyboardButton("Kulgili ovozlar 😆"), KeyboardButton("Tabriklar 🎉")],
        [KeyboardButton("She'rlar 📚"), KeyboardButton("🏆 Top ovozlar")],
        [KeyboardButton("🎤 Ovoz qo'shish ➕")]
    ], resize_keyboard=True)