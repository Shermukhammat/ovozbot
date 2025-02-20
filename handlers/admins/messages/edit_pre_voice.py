from loader import bot, dp, db, register_sema
from aiogram import types
from aiogram.dispatcher import FSMContext
from data import User, PreVoice, Voice
from uuid import uuid4
from buttons import InlineKeyboards, Keyboards
from utilites import shoud_edit, AdminStates
from datetime import datetime


@dp.message_handler(state=AdminStates.edit_prevoice)
async def edit_prevoice(update: types.Message, state: FSMContext):
    await state.reset_state()
    await update.answer("✅ Ovozni qo'shish bekor qilndi", reply_markup=Keyboards.admin_home_menu)


@dp.message_handler(state=AdminStates.edit_prevoice_title)
async def edit_prevoice_title(update: types.Message, state: FSMContext):
    state_data = await state.get_data()
    pr : PreVoice = state_data['pr']

    if update.text == "⬅️ Orqaga":
        await state.set_state(AdminStates.edit_prevoice)
        await bot.copy_message(chat_id=update.from_user.id,
                                   message_id=pr.message_id,
                                   reply_markup=InlineKeyboards.pre_voice_acepting(),
                                   caption = f'🆕 Nomi: {pr.title} \n🧩 Tag: {pr.tag}',
                                   from_chat_id=db.DATA_CHANEL_ID)
        
    elif len(update.text) <= 40 and len(update.text) >= 5:
        await state.set_state(AdminStates.edit_prevoice)
        pr.title = update.text
        await state.update_data(pr = pr)

        await bot.copy_message(chat_id=update.from_user.id,
                                   message_id=pr.message_id,
                                   reply_markup=InlineKeyboards.pre_voice_acepting(),
                                   caption = f'🆕 Nomi: {pr.title} \n🧩 Tag: {pr.tag}',
                                   from_chat_id=db.DATA_CHANEL_ID)
    
    else:
        await update.reply("❌ Ovoz nomni 5 ta belgidan kam va 40 ta belgidan ko'p bo'lishi mumkun emas", reply_markup=Keyboards.back_button)


@dp.message_handler(state=AdminStates.edit_prevoice_tag)
async def edit_prevoice_tag(update: types.Message, state: FSMContext):
    state_data = await state.get_data()
    pr : PreVoice = state_data['pr']

    if update.text == "⬅️ Orqaga":
        await state.set_state(AdminStates.edit_prevoice)
        await bot.copy_message(chat_id=update.from_user.id,
                                   message_id=pr.message_id,
                                   reply_markup=InlineKeyboards.pre_voice_acepting(),
                                   caption = f'🆕 Nomi: {pr.title} \n🧩 Tag: {pr.tag}',
                                   from_chat_id=db.DATA_CHANEL_ID)
        
    elif len(update.text) <= 70 and len(update.text) >= 5:
        await state.set_state(AdminStates.edit_prevoice)
        pr.tag = update.text
        await state.update_data(pr = pr)

        await bot.copy_message(chat_id=update.from_user.id,
                                   message_id=pr.message_id,
                                   reply_markup=InlineKeyboards.pre_voice_acepting(),
                                   caption = f'🆕 Nomi: {pr.title} \n🧩 Tag: {pr.tag}',
                                   from_chat_id=db.DATA_CHANEL_ID)
    
    else:
        await update.reply("❌ Ovoz tegi 5 ta belgidan kam va 70 ta belgidan ko'p bo'lishi mumkun emas", reply_markup=Keyboards.back_button)