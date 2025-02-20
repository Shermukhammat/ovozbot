from loader import bot, dp, db, register_sema
from aiogram import types
from aiogram.dispatcher import FSMContext
from data import User, Voice, PreVoice
from uuid import uuid4
from buttons import InlineKeyboards, Keyboards
from utilites import register_user, UserStates
from uuid import uuid4
import os 




@dp.message_handler(content_types=types.ContentType.AUDIO)
async def user_audio_handler(update : types.Message, state: FSMContext):
    if update.via_bot and update.via_bot.username == db.bot.username:
        return
    
    pr = PreVoice(user_id = update.from_user.id, username = update.from_user.username)
    
    await state.set_state(UserStates.get_voice_name)
    size = update.audio.file_size / 1024 / 1024

    if size > 10:
        await update.reply("❌ Ovoz hajmi 10mb dan kam bo'lishi kerak", reply_markup=Keyboards.user_home_menu)
        return
    await state.set_data({'pr':pr, 'file_id' : update.audio.file_id, 'voice': False})
    
    await update.reply("✅ Ok, oxirgi ish ovoz nomini kirting", reply_markup=Keyboards.back_button)


@dp.message_handler(content_types=types.ContentType.VOICE)
async def user_voice_handler(update : types.Message, state : FSMContext):
    if update.via_bot and update.via_bot.username == db.bot.username:
        return
    
    
    pr = PreVoice(user_id = update.from_user.id, username = update.from_user.username)
    
    await state.set_state(UserStates.get_voice_name)
    await state.set_data({'pr':pr, 'file_id' : update.voice.file_id, 'voice': True})
    
    await update.reply("✅ Ok, oxirgi ish ovoz nomini kirting", reply_markup=Keyboards.back_button)
    