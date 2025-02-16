from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup



class InlineKeyboards:
    def search_voice(query: str | None = "") -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton("🔍 Ovoz izlash", switch_inline_query_current_chat=query)]]
            )
    
    def voice_buttons(id : int, query : str) -> InlineKeyboardButton:
        if query:
            search_text = "▶️ Davom ettirish"
        else:
            search_text = "🔍 Ovoz izlash"
 
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton("❤️/💔", callback_data=f'like&{id}'), InlineKeyboardButton('❌', callback_data='remove')],
            [InlineKeyboardButton(search_text, switch_inline_query_current_chat=query)]
            ])