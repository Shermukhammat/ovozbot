from loader import bot, dp, db, register_sema
from aiogram import types
from aiogram.dispatcher import FSMContext
from data import User, Voice
from uuid import uuid4
from buttons import InlineKeyboards
from utilites import register_user



async def user_inline_search(update: types.InlineQuery):
    is_sender = update.chat_type == 'sender'
    if len(update.query) > 3:
        voices = await db.search_voices(update.query)
        if voices:
            await update.answer([inline_voice(voice, is_sender, update.query) for voice in voices], cache_time = db.INLINE_CACHE_TIME, is_personal = True)
        else:
            await update.answer([nofound("Hechnarsa topilmadi")], cache_time = db.INLINE_CACHE_TIME, is_personal = True)

    # else:
    #     voices = await db.get_top_voices()
    #     if voices:
    #         await update.answer([inline_voice(voice, is_sender, update.query) for voice in voices], cache_time = db.INLINE_CACHE_TIME, is_personal = True)
    #     else:
    #         await update.answer([nofound("Hozirda botda birortaxam ovoz yo'q")], cache_time = db.INLINE_CACHE_TIME, is_personal = True)


async def non_user_inline_search(update: types.InlineQuery):
    if update.chat_type == 'sender':
        await register_user(update.from_user.id, update.from_user.first_name)
        await user_inline_search(update)
    
    else:
        input_register = types.InputTextMessageContent(message_text=f"❗️ Ro'yxatdan o'tish uchun botga o'tib startni bosishingiz kerak")
        got_to_bot = types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton("✅ Botga o'tish", url=f"https://t.me/{db.bot.username}?start=blah")]])
        need_registration = [types.InlineQueryResultArticle(id="needcommandstart",
                                    title="❗️ Ro'yxatdan o'tmagansiz",
                                    description = "➡️ Buyerga bosing",
                                    input_message_content=input_register,
                                    reply_markup = got_to_bot,
                                    thumb_url=db.LOGO_URL)]

        await update.answer(need_registration, cache_time = 10, is_personal = True)



input_content = types.InputTextMessageContent(f"So'rovingiz boyicha hechnarsa topilmadi")

def inline_voice(voice : Voice, is_sender : bool | None = True, query : str | None = None) -> types.InlineQueryResultVoice:
    if is_sender:
        return types.InlineQueryResultVoice(id = voice.str_id, voice_url=voice.url, title = voice.title, 
                                            caption = f"🎙 Nomi: {voice.title} \n🧩 Teg: {voice.tag}",
                                            reply_markup = InlineKeyboards.voice_buttons(voice.id, query))
    
    return types.InlineQueryResultVoice(id = voice.str_id, voice_url=voice.url, title = voice.title)
    
def nofound(title : str | None = "Hechnarsa topilmadi", 
            description : str | None = None, 
            input_content : types.InputMessageContent | None = input_content):
    return types.InlineQueryResultArticle(id='nothingfoundid',
                                    title=title,
                                    description = description,
                                    input_message_content = input_content,
                                    thumb_url=db.NO_FOUND_URL)

