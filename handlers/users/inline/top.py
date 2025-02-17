from loader import bot, dp, db, register_sema
from aiogram import types
from aiogram.dispatcher import FSMContext
from data import User, Voice
from buttons import InlineKeyboards



async def user_inline_top(update: types.InlineQuery):
    is_sender = update.chat_type == 'sender'

    voices = await db.get_top_voices()
    if voices:  
        # print(voices)
        await update.answer([inline_voice(voice, is_sender, update.query) for voice in voices], cache_time = 10, is_personal = True) 

    else:
        await update.answer([nofound("🤷🏻‍♂️ Topda birotaham ovoz yoq")], cache_time = 10, is_personal = True)


input_content = types.InputTextMessageContent(f"So'rovingiz boyicha hechnarsa topilmadi")

def inline_voice(voice : Voice, is_sender : bool | None = True, query : str | None = '') -> types.InlineQueryResultVoice:
    if is_sender:
        return types.InlineQueryResultVoice(id = voice.str_id, voice_url=voice.url, title = voice.title, 
                                            caption = f"🎙 Nomi: {voice.title} \n🧩 Teg: {voice.tag} \n🎧 {voice.in_playlist} ta foydlanuvchi playlistida",
                                            reply_markup=InlineKeyboards.voice_buttons(voice.id, query))
    
    return types.InlineQueryResultVoice(id = voice.str_id, voice_url=voice.url, title = voice.title)

def nofound(title : str | None = "Hechnarsa topilmadi", 
            description : str | None = None, 
            input_content : types.InputMessageContent | None = input_content):
    return types.InlineQueryResultArticle(id='nothingfoundid',
                                    title=title,
                                    description = description,
                                    input_message_content = input_content,
                                    thumb_url=db.NO_FOUND_URL)