from loader import bot, dp, db 
from data import Admin
from aiogram import types
from aiogram.dispatcher import FSMContext
from .users.inline import user_inline_search, non_user_inline_search, user_inline_playlist, user_inline_top
from .admins.inline import admin_inline_search, admin_inline_playlist, admin_inline_top
from .users.callback import user_callback_handler
from .admins.callback import admin_callback_handler
from .users.commands import user_menu_command_hanlder, user_admin_command_hanlder, user_start_hanlder
from .users.messages import user_text_handler
from .admins.messages import admin_text_handler
from uuid import uuid4
from utilites import register_user
import os


    

@dp.inline_handler(lambda update : update.query.startswith('#top'), state='*')
async def inline_top_filter(update : types.InlineQuery, state : FSMContext):
    if update.query != '#top':
        pass

    elif await db.is_user(update.from_user.id):
        await user_inline_top(update)

    elif await db.is_admin(update.from_user.id):
        await admin_inline_top(update)

    else:
        await non_user_inline_search(update)    


@dp.inline_handler(lambda update : update.query.startswith('#pl'), state='*')
async def inline_playlist_filter(update : types.InlineQuery):
    if update.query != '#pl':
        pass
    
    elif await db.is_user(update.from_user.id):
        await user_inline_playlist(update)

    elif await db.is_admin(update.from_user.id):
        await admin_inline_playlist(update)

    else:
        await non_user_inline_search(update)


@dp.inline_handler(state='*')
async def inline_filter(update : types.InlineQuery, state : FSMContext):
    user = await db.get_user(update.from_user.id)
    if user:
        await user_inline_search(update)

    elif await db.is_admin(update.from_user.id):
        await admin_inline_search(update)

    else:
        await non_user_inline_search(update)


@dp.callback_query_handler()
async def callback_filter(update : types.CallbackQuery, state : FSMContext):
    if await db.is_user(update.from_user.id):
        await user_callback_handler(update)

    elif await db.is_admin(update.from_user.id):
        await admin_callback_handler(update, state)

    else:
        await register_user(update.from_user.id, update.from_user.first_name)




@dp.message_handler(commands='start')
async def start_filter(update : types.Message, state : FSMContext):
    if await db.is_user(update.from_user.id):
        await user_start_hanlder(update)

    elif await db.is_admin(update.from_user.id):
        pass

    else:
        await register_user(update.from_user.id, update.from_user.first_name)

@dp.message_handler(commands='menyu')
async def command_menu_filter(update: types.Message):
    if await db.is_user(update.from_user.id):
        await user_menu_command_hanlder(update)

    elif await db.is_admin(update.from_user.id):
        pass

    else:
        await register_user(update.from_user.id, update.from_user.first_name)


@dp.message_handler(commands='admin')
async def command_admin_filter(update: types.Message):
    if await db.is_admin(update.from_user.id):
        await user_admin_command_hanlder(update)
    else:
        await user_admin_command_hanlder(update)


@dp.message_handler()
async def text_filter(update : types.Message, state : FSMContext):
    user =  await db.is_user(update.from_user.id)
    if user:
        await user_text_handler(update, user)

    elif await db.is_admin(update.from_user.id):
        await admin_text_handler(update)

    else:
        await register_user(update.from_user.id, update.from_user.first_name)
