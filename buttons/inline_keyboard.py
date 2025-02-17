from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup



class InlineKeyboards:
    show_top = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton("🏆 Top ovozlar", switch_inline_query_current_chat="#top")]]
            ) 
    playlist = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton("⭐️ Playlist", switch_inline_query_current_chat="#pl")]]
            )
    edit_help_content = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton("🔄 O'zgartirish", callback_data = "edit_help_content")]]
            )
    def search_voice(query: str | None = "") -> InlineKeyboardMarkup:
        if query:
            return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton("▶️ Ko'rish", switch_inline_query_current_chat=query)]]
            )
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton("🔍 Ovoz izlash", switch_inline_query_current_chat=query)]]
            )
    
    def voice_buttons(id : int, query : str | None = "") -> InlineKeyboardButton:
        if query:
            search_text = "▶️ Davom ettirish"
        else:
            search_text = "🔍 Ovoz izlash"
 
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton("❤️/💔", callback_data=f'like&{id}'), InlineKeyboardButton('❌', callback_data='remove')],
            [InlineKeyboardButton(search_text, switch_inline_query_current_chat=query)]
            ])