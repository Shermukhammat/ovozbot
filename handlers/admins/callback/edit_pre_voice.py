from loader import bot, dp, db, register_sema
from aiogram import types
from aiogram.dispatcher import FSMContext
from data import User, PreVoice, Voice
from uuid import uuid4
from buttons import InlineKeyboards, Keyboards
from utilites import shoud_edit, AdminStates



@dp.callback_query_handler(state=AdminStates.edit_prevoice)
async def edit_prevoice(update: types.CallbackQuery, state: FSMContext):
    if update.data == 'back':
        state_data = await state.get_data()
        await state.reset_state()

        pr : PreVoice = state_data['pr']
        user = await db.get_user(pr.user_id)
        if user:
            name = user.name
        else:
            name = "👻 O'chirlgan hisob"

        if shoud_edit(update.message.date):
            await update.message.edit_caption(f"🆕 Nomi: {pr.title} \n👤 Foydalanuvchi: {name} {'@'+pr.username if pr.username else ''} \n📆 Yuborildi: {pr.readble_time}",
                                              reply_markup = InlineKeyboards.pre_voice(pr))
        
        else:
            await bot.copy_message(chat_id=update.from_user.id,
                                   message_id=pr.message_id,
                                   reply_markup=InlineKeyboards.pre_voice(pr),
                                   caption = f"🆕 Nomi: {pr.title} \n👤 Foydalanuvchi: {name} {'@'+pr.username if pr.username else ''} \n📆 Yuborildi: {pr.readble_time}",
                                   from_chat_id=db.DATA_CHANEL_ID)
    
    elif update.data == 'title':
        await state.set_state(AdminStates.edit_prevoice_title)
        await update.message.answer("📝 Ovoz uchun yangi nomni yuboring", reply_markup=Keyboards.back_button)

    elif update.data == 'tag':
        await state.set_state(AdminStates.edit_prevoice_tag)
        await update.message.answer("📝 Ovoz uchun yangi tegni kirting", reply_markup=Keyboards.back_button)
    
    elif update.data == 'done':
        state_data = await state.get_data()
        await state.reset_state()

        pr : PreVoice = state_data['pr']
        await db.add_voice(Voice(title=pr.title, tag=pr.tag, message_id=pr.message_id, url=pr.url))
        await db.delete_pre_voice(pr.id)

        await update.answer("✅ Ovoz qo'shildi", show_alert = True)

        if shoud_edit(update.message.date):
            await update.message.edit_reply_markup()

        
    