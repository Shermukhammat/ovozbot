from loader import bot, dp, db, register_sema
from aiogram import types
from data import User
from aiogram.utils.markdown import escape_md
from buttons import Keyboards, InlineKeyboards
from random import choice

async def user_start_hanlder(update : types.Message):
    user = await db.get_user(update.from_user.id)
    if not user:
        return
    
    await update.answer(f"👤 Foydalanuvchi: [{user.safe_name}]({update.from_user.url}). \n⏳ Ro'yxatdan o'tdi: {user.registred_readble}",
                        parse_mode=types.ParseMode.MARKDOWN,
                        reply_markup = Keyboards.user_home_menu)

