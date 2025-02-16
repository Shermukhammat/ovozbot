from aiogram import types
from loader import register_sema, db, bot 
from random import choice
from data import User
from buttons import InlineKeyboards, Keyboards
from aiogram.utils.markdown import escape_md


async def register_user(user_id : int, name : str):
    async with register_sema:
        if await db.is_user(user_id):
            pass

        elif not await db.is_admin(user_id):
            message_id = choice([33, 34, 37])
            await bot.copy_message(chat_id=user_id, from_chat_id=db.DATA_CHANEL_ID, message_id = message_id, 
                                   reply_markup = Keyboards.user_home_menu)
            user = User(id = user_id, name = name)
            await db.register_user(user)

            await bot.send_message(text = f"Assalomu alaykum [{user.safe_name}](tg://user?id={user_id}). Men [{escape_md(db.bot.first_name)}]({db.bot.url}) man. Men sizga qizqarli ovzlarni topishga yordam beraman",
                                   chat_id=user_id,
                                   reply_markup=InlineKeyboards.search_voice(),
                                   parse_mode=types.ParseMode.MARKDOWN)