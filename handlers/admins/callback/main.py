from loader import bot, dp, db, register_sema
from aiogram import types
from aiogram.dispatcher import FSMContext
from data import User, Voice, PreVoice
from uuid import uuid4
from buttons import InlineKeyboards
from utilites import shoud_edit, AdminStates
from datetime import datetime


async def admin_callback_handler(update: types.CallbackQuery, state: FSMContext):
    # print(update.data)
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
        voice_id = update.data.replace('pr', '')
        if voice_id.isnumeric():
            pr = await db.get_pre_voice(int(voice_id))
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
            else:
                await update.answer("❌ Ovoz topilmadi", show_alert = True)
    
    elif update.data.startswith('aceptpr'):
        voice_id = update.data.replace('aceptpr', '')
        if voice_id.isnumeric():
            pr = await db.get_pre_voice(int(voice_id))
            if pr:
                await state.set_state(AdminStates.edit_prevoice)
                await state.set_data({'pr':pr})
                if shoud_edit(update.message.date):
                    await update.message.edit_caption(f'🆕 Nomi: {pr.title} \n🧩 Tag: {pr.tag}',
                                                      reply_markup=InlineKeyboards.pre_voice_acepting()) 

            else:
                await update.answer("❌ Ovoz topilmadi", show_alert = True) 

    elif update.data.startswith('next'):
        offset = update.data.replace('next', '')
        if not offset.isnumeric():
            return
        
        offset = int(offset)
        voices = await db.get_pre_voices(offset)
        if voices:
            text = await pre_voices_list_text(voices, offset)
            if shoud_edit(update.message.date):
                await update.message.edit_text(text, reply_markup=InlineKeyboards.pre_voices(voices, offset, await db.prevoices_leng))
        
        else:
            await update.answer("❌ Boshqa sahifa yo'q", show_alert = True)

    elif update.data.startswith('delpr'):
        voice_id = update.data.replace('delpr', '')
        if voice_id.isnumeric():
            voice_id = int(voice_id)  
            await db.delete_pre_voice(voice_id)
            await update.answer("✅ Ovoz o'chirildi", show_alert = True)

    elif update.data == 'no_next':
        await update.answer("❌ Boshqa sahifa yo'q", show_alert = True)

    elif update.data == 'remove':
        if update.message and shoud_edit(update.message.date):
            await update.message.delete()
    
    else:
        await update.answer("❌ Noma'lum buyruq", show_alert = True)

async def pre_voices_list_text(voices : list[PreVoice], offset : int | None = 0, limit : int | None = 10) -> str:
    text = f"Natijalar {offset+1}-{offset+limit if offset > 10 else len(voices)}  {await db.prevoices_leng} dan"
    for index, voice in enumerate(voices):        
        if voice.username:
            text += f"\n{index+1}. {voice.title}"
        else:
            text += f"\n{index+1}. {voice.title}"
    
    return text