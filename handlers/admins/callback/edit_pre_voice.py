from loader import bot, dp, db, register_sema
from aiogram import types
from aiogram.dispatcher import FSMContext
from data import User, PreVoice
from uuid import uuid4
from buttons import InlineKeyboards
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