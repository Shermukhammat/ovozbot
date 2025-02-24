from loader import bot, dp, db, register_sema
from aiogram import types
from aiogram.dispatcher import FSMContext
from data import User, Voice, PreVoice
from uuid import uuid4
from buttons import InlineKeyboards, Keyboards
from utilites import shoud_edit, AdminStates
from datetime import datetime


@dp.callback_query_handler(state=AdminStates.delete_voice)
async def delete_voice(update: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    token = state_data.get('token')
    vs : Voice = state_data.get('vs')
    
    if update.data == token:
        await db.remove_voice(vs.id)
        async with db.paramas_sem:
            if vs.id in db.PINED_VOICES:
                db.PINED_VOICES.remove(vs.id)
                db.params_data['pined_voices']= db.PINED_VOICES
                db.update_params()
        
        await update.answer("✅ Ovoz o'chirb tashlandi", show_alert=True)
        await state.reset_state()
        if update.message:
            await update.message.delete()
    
    else:
        await update.answer("✅ Ovozni o'chrish bekor qilndi", show_alert=True)
        await state.reset_state()
        if update.message:
            await update.message.delete()