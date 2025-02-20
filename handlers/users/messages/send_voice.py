from loader import bot, dp, db, register_sema
from aiogram import types
from aiogram.dispatcher import FSMContext
from data import User, Voice, PreVoice
from uuid import uuid4
from buttons import InlineKeyboards, Keyboards
from utilites import register_user, UserStates
import os



@dp.message_handler(state=UserStates.get_voice_name)
async def user_text_handler(update : types.Message, state : FSMContext):
    if update.text == "⬅️ Orqaga":
        await state.reset_state()
        await update.answer("🎛 Bosh menyu", reply_markup = Keyboards.user_home_menu)

    elif len(update.text) >= 5 and len(update.text) <= 64:
        state_data = await state.get_data()
        await state.reset_state()

        await update.reply("✅ Adminga yuborildi, ovoz admin tomonidan tekshirlgach botga qoshiladi",
                           reply_markup=Keyboards.user_home_menu)
        
        if state_data['voice']:
            pr : PreVoice = state_data['pr']
            file_id : str = state_data['file_id']

            try:
                file = await bot.get_file(file_id)
            except:
                # await update.answer("😩 Ovozni o'chirb tashlagan ko'rnasiz, adminga yubora olmadim",
                #            reply_markup=Keyboards.user_home_menu)
                return
            
            mim_type = file.file_path.split('.')[-1]
            file_name = f"{uuid4().hex}.{mim_type}"
            await file.download(destination_file=f'data/voices/{file_name}')

            message_data = await bot.send_voice(chat_id=db.DATA_CHANEL_ID, 
                                                voice=open(f'data/voices/{file_name}', 'rb'), 
                                                caption='blah test')
            os.remove(f'data/voices/{file_name}')

            pr.message_id = message_data.message_id
            pr.url = message_data.voice.file_id
            pr.title = update.text
            await db.add_pre_voice(pr)
    
    else:
        await update.reply("❌ Ovoz nomi 5ta belgidan kam va 64ta belgidan ko'p bo'lmasligi kerak",
                           reply_markup=Keyboards.back_button)