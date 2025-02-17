from loader import bot, dp, db, register_sema
from aiogram import types
from data import User
from aiogram.utils.markdown import escape_md
from buttons import Keyboards, InlineKeyboards
from random import choice
from utilites import register_user

@dp.message_handler(commands='yordam')
async def playlis_command(update : types.Message):
    if await db.is_user(update.from_user.id):
        await bot.copy_message(chat_id=update.from_user.id,
                               from_chat_id=db.DATA_CHANEL_ID,
                               message_id=db.HELP_CONTENT)
    
    elif await db.is_admin(update.from_user.id):
        await bot.copy_message(chat_id=update.from_user.id,
                               from_chat_id=db.DATA_CHANEL_ID,
                               reply_markup=InlineKeyboards.edit_help_content,
                               message_id=db.HELP_CONTENT)

    else:
        await register_user(update.from_user.id, update.from_user.first_name)