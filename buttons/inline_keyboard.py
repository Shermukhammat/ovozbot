from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup



class InlineKeyboards:
    def search_voice(query: str | None = "") -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton("🔍 Ovoz izlash", switch_inline_query=query)]])