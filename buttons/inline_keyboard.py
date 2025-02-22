from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from data import PreVoice


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
            search_text = "▶️ Davom"
        else:
            search_text = "🔍 Izlash"
 
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton("❤️/💔", callback_data=f'{id}'), InlineKeyboardButton(search_text, switch_inline_query_current_chat=query)],
            # [InlineKeyboardButton(search_text, switch_inline_query_current_chat=query)]
            ])
    
    def admin_voice_buttons(id : int, query : str | None = "") -> InlineKeyboardButton:
        if query:
            search_text = "▶️ Davom ettirish"
        else:
            search_text = "🔍 Ovoz izlash"
 
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton("❤️/💔", callback_data=f'{id}'), InlineKeyboardButton("📌 Pin", callback_data=f'pin{id}')],
            [InlineKeyboardButton("✏️ Tahrirlash", callback_data=f'edit{id}'), InlineKeyboardButton("🗑 O'chirish", callback_data=f'del{id}')],
            [InlineKeyboardButton(search_text, switch_inline_query_current_chat=query)]
            ])
    
    def pre_voices(voices : list[PreVoice], offset : int | None = 0, leng : int | None = 10) -> InlineKeyboardButton:
        if len(voices) < 6:
            buttons = [[InlineKeyboardButton(str(index+1), callback_data=f"pr{voice.id}") for index, voice in enumerate(voices)]]
        else:
            buttons = [[InlineKeyboardButton(str(index+1), callback_data=f"pr{voice.id}") for index, voice in enumerate(voices[:5])],
                       [InlineKeyboardButton(str(index+6), callback_data=f"pr{voice.id}") for index, voice in enumerate(voices[5:])]]

        if offset + 10 < leng:
            next = f"next{offset+10}"
        else:
            next = f"no_next"
        
        if offset < 10:
            back = 'no_next'
        else:
            back = f"next{offset - 10}"

        buttons.append([InlineKeyboardButton("⬅️", callback_data = back), InlineKeyboardButton("❌", callback_data = 'remove'), InlineKeyboardButton("➡️", callback_data = next)])
        return InlineKeyboardMarkup(inline_keyboard = buttons)
    

    def pre_voice(voice: PreVoice) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton("✅ Qo'shish", callback_data = f'aceptpr{voice.id}'), InlineKeyboardButton("🗑 O'chrish", callback_data=f'delpr{voice.id}')],
            [InlineKeyboardButton("❌", callback_data = 'remove')]
        ])
    
    def pre_voice_acepting() -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton("✏️ Nomi", callback_data = f'title'), InlineKeyboardButton("✏️ Tegi", callback_data=f'tag')],
            [InlineKeyboardButton("⬅️ Orqaga", callback_data = 'back'), InlineKeyboardButton("✅ Tayyor", callback_data = 'done')],
        ])