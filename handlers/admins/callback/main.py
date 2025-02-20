from loader import bot, dp, db, register_sema
from aiogram import types
from aiogram.dispatcher import FSMContext
from data import User, Voice
from uuid import uuid4
from buttons import InlineKeyboards
from utilites import shoud_edit, AdminStates
from datetime import datetime


async def admin_callback_handler(update: types.CallbackQuery, state: FSMContext):
    if update.data.isnumeric():
        voice_id = int(update.data)
        playlist = await db.get_playlist(update.from_user.id)


        if voice_id in playlist:
            await db.remove_voice_from_playlist(update.from_user.id, voice_id)
            await update.answer("✅ Ovoz playlistingizdan olib tashlandi", show_alert = True)

        elif len(playlist) > 45:
            await update.answer("❌ Playlistingizga 45 tadan kop ovoz qo'sha olmaysiz", show_alert = True)
        
        else:
            await db.add_voice_to_playlist(update.from_user.id, voice_id)
            await update.answer("✅ Ovoz playlistingizga qo'shildi", show_alert = True)
    
    elif update.data.startswith('pr'):
        id = update.data.replace('pr', '')
        if id.isnumeric():
            pr = await db.get_pre_voice(int(id))
            if pr:
                user = await db.get_user(pr.user_id)
                if user:
                    name = user.name
                else:
                    name = "👻 O'chirlgan hisob"

                await bot.copy_message(chat_id=update.from_user.id,
                                       message_id=pr.message_id,
                                       reply_markup=InlineKeyboards.pre_voice(pr),
                                       caption = f"🆕 Nomi: {pr.title} \n👤 Foydalanuvchi: {name} {'@'+pr.username if pr.username else ''} \n📆 Yuborildi: {pr.readble_time}",
                                       from_chat_id=db.DATA_CHANEL_ID)
    
    elif update.data.startswith('aceptpr'):
        id = update.data.replace('aceptpr', '')
        if id.isnumeric():
            pr = await db.get_pre_voice(int(id))
            if pr:
                await state.set_state(AdminStates.edit_prevoice)
                await state.set_data({'pr':pr})
                if shoud_edit(update.message.date):
                    await update.message.edit_caption(f'🆕 Nomi: {pr.title} \n🧩 Tag: {pr.tag}',
                                                      reply_markup=InlineKeyboards.pre_voice_acepting())  
                
    # elif update.data == 'remove':
    #     if shoud_edit(update):
    #         await update.message.delete()