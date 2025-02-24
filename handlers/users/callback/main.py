from loader import bot, dp, db, register_sema
from aiogram import types
from aiogram.dispatcher import FSMContext
from data import User, Voice
from uuid import uuid4
from buttons import InlineKeyboards, Keyboards
from utilites import shoud_edit


async def user_callback_handler(update: types.CallbackQuery):
    if update.data.isnumeric():
        voice_id = int(update.data)
        playlist = await db.get_playlist_ids(update.from_user.id)


        if voice_id in playlist:
            await db.remove_voice_from_playlist(update.from_user.id, voice_id)
            await update.answer("✅ Ovoz playlistingizdan olib tashlandi", show_alert = True)

        elif len(playlist) > 195:
            await update.answer("❌ Playlistingizga 200 tadan kop ovoz qo'sha olmaysiz", show_alert = True)
        
        else:
            await db.add_voice_to_playlist(update.from_user.id, voice_id)
            await update.answer("✅ Ovoz playlistingizga qo'shildi", show_alert = True)
    
    elif update.data == 'remove' :
        if update.message and shoud_edit(update.message.date):
            await update.message.delete()
    
    elif update.data == 'check_sub':
        if update.message:
            await update.message.answer("✅ Botdan foydalnishingiz mumkun", reply_markup=Keyboards.user_home_menu)


        if update.message and shoud_edit(update.message.date):
            await update.message.delete()