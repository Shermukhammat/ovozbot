from loader import bot, dp, db, register_sema
from aiogram import types
from data import User
from aiogram.utils.markdown import escape_md
from random import choice

async def user_start_hanlder(update : types.Message):
    user = await db.get_user(update.from_user.id)
    if not user:
        return
    
    await update.answer(f"👤 Foydalanuvchi: [{user.safe_name}]({update.from_user.url}). \n⏳ Ro'yxatdan o'tdi: {user.registred_readble}",
                                parse_mode=types.ParseMode.MARKDOWN)


async def user_register_hanlder(update : types.Message):
    async with register_sema:
        if await db.is_user(update.from_user.id):
            await user_start_hanlder(update)

        elif not await db.is_admin(update.from_user.id):
            message_id = choice([33, 34, 37])
            await bot.copy_message(chat_id=update.from_user.id, from_chat_id=db.DATA_CHANEL_ID, message_id = message_id)
            user = User(id = update.from_user.id, name = update.from_user.first_name)
            await db.register_user(user)

            await update.answer(f"Assalomu alaykum [{user.safe_name}]({update.from_user.url}). Men [{escape_md(db.bot.first_name)}]({db.bot.url}) man. Men sizga qizqarli ovzlarni topishga yordam beraman",
                                parse_mode=types.ParseMode.MARKDOWN)