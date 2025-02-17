from loader import bot, dp, db, register_sema
from aiogram import types
from data import User
from aiogram.utils.markdown import escape_md
from buttons import Keyboards, InlineKeyboards
from random import choice
from utilites import register_user

@dp.message_handler(commands='playlist')
async def playlis_command(update : types.Message):
    if await db.is_user(update.from_user.id) or await db.is_admin(update.from_user.id):
        await update.reply("👇 Playlistingizni ko'rish uchun pastdagi tugmani bosing", reply_markup = InlineKeyboards.playlist)
    
    else:
        await register_user(update.from_user.id, update.from_user.first_name)