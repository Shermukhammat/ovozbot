from loader import bot, dp, db, register_sema
from aiogram import types
from aiogram.dispatcher import FSMContext
from data import User, PreVoice
from uuid import uuid4
from buttons import InlineKeyboards, Keyboards
from utilites import register_user



async def admin_text_handler(update : types.Message):
    if update.text == "🏆 Top ovozlar":
        await update.answer("👇 Top ovozlarni ko'rish uchun pastdagi tugmani bosing", reply_markup = InlineKeyboards.show_top)
    
    elif update.text == "🔍 Ovoz izlash":
        await update.answer("👇 Ovoz izlash uchun pastdagi tugmani bosing", reply_markup = InlineKeyboards.search_voice())

    elif update.text == "⭐️ Playlist":
        await update.reply("👇 Playlistingizni ko'rish uchun pastdagi tugmani bosing", reply_markup = InlineKeyboards.playlist)
    
    elif update.text == "📖 Yordam":
        await bot.copy_message(chat_id=update.from_user.id,
                               from_chat_id=db.DATA_CHANEL_ID,
                               message_id=db.HELP_CONTENT)

    elif update.text == "🆕 Yangi ovozlar":
        voices = await db.get_pre_voices()
        if voices:
            text = pre_voices_list_text(voices)
            await update.answer(text, reply_markup=InlineKeyboards.pre_voices(voices))

        else:
            await update.answer("🤷🏻‍♂️ Xoizrda birotaham ovoz yoq")

    elif len(update.text) > 2:
        await update.reply("🔍 Natijalarni ko'rish uchun pastdagi tugamani bosing",
                            reply_markup = InlineKeyboards.search_voice(update.text))
    
    else:
        await update.answer("🎛 Bosh menyu", reply_markup = Keyboards.admin_home_menu)



def pre_voices_list_text(voices : list[PreVoice], offset : int | None = 0, limit : int | None = 10) -> str:
    text = f"Natijalar {offset+1}-{offset+limit if offset > 10 else len(voices)}"
    for index, voice in enumerate(voices):        
        if voice.username:
            text += f"\n{index+1}. {voice.title}"
        else:
            text += f"\n{index+1}. {voice.title}"
    
    return text