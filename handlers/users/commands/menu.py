from loader import bot, dp, db, register_sema
from aiogram import types
from data import User
from aiogram.utils.markdown import escape_md
from buttons import Keyboards, InlineKeyboards
from random import choice

async def user_menu_command_hanlder(update : types.Message):
    await update.reply("🎛 Bosh menyu", reply_markup = Keyboards.user_home_menu)

