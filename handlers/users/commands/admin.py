from loader import bot, dp, db, register_sema
from aiogram import types
from data import Admin
from aiogram.utils.markdown import escape_md
from buttons import Keyboards, InlineKeyboards
from random import choice

async def user_admin_command_hanlder(update : types.Message):
    if await db.is_admin(update.from_user.id):
        admin = await db.get_admin(update.from_user.id)
        await update.answer(f"👤 Admin: [{admin.safe_name}]({update.from_user.url}). \n⏳ Ro'yxatdan o'tdi: {admin.registred_readble}",
                        parse_mode=types.ParseMode.MARKDOWN,
                        reply_markup = Keyboards.admin_home_menu)
        
    elif update.from_user.id in db.DEV_ID:
        async with register_sema:
            if await db.is_admin(update.from_user.id):
                admin = await db.get_admin(update.from_user.id)
                await update.answer(f"👤 Admin: [{admin.safe_name}]({update.from_user.url}). \n⏳ Ro'yxatdan o'tdi: {admin.registred_readble}",
                                    parse_mode=types.ParseMode.MARKDOWN,
                                    reply_markup = Keyboards.admin_home_menu)
            else:
                await db.remove_user(update.from_user.id)
                admin = Admin(id=update.from_user.id, name=update.from_user.first_name)
                await db.register_admin(admin)

                await update.answer(f"👤 Admin: [{admin.safe_name}]({update.from_user.url}). \n⏳ Ro'yxatdan o'tdi: {admin.registred_readble}",
                        parse_mode=types.ParseMode.MARKDOWN,
                        reply_markup = Keyboards.admin_home_menu)
            
            

