from loader import bot, dp, db, register_sema
from aiogram import types
from aiogram.dispatcher import FSMContext
from data import User, Voice
from uuid import uuid4
from buttons import InlineKeyboards, Keyboards
from utilites import register_user



async def user_text_handler(update : types.Message, user : User):
    if update.text == "Kulgili ovozlar 😆":
        await update.answer("Kulgili ovozlar menyusi", reply_markup=Keyboards.kulgili_ovozlar)
    
    elif update.text == "Tabriklar 🎉":
        await update.answer("Tabriklar menyusi", reply_markup=Keyboards.tabriklar)
    
    elif update.text == "She'rlar 📚":
        await update.answer("She'rlar menyusi", reply_markup=Keyboards.sherlar)

    elif db.ovozlar_data.get(update.text):
        voice_id = db.ovozlar_data.get(update.text)
        voice = await db.get_voice(voice_id)
        if voice:
            await bot.copy_message(chat_id=update.from_user.id,
                                   message_id = voice.message_id,
                                   caption = f"🎙 Nomi: {voice.title} \n🧩 Teg: {voice.tag}",
                                   reply_markup = InlineKeyboards.voice_buttons(voice.id),
                                   from_chat_id = db.DATA_CHANEL_ID)
    
    elif update.text == "⬅️ Orqaga":
        await update.answer("🎛 Bosh menyu", reply_markup = Keyboards.user_home_menu)

    elif len(update.text) > 2:
        await update.reply("🔍 Natijalarni ko'rish uchun pastdagi tugamani bosing",
                            reply_markup = InlineKeyboards.search_voice(update.text))
    
    else:
        await update.answer("🎛 Bosh menyu", reply_markup = Keyboards.user_home_menu)