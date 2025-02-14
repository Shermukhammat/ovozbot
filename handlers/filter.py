from loader import bot, dp, db 
from aiogram import types
from aiogram.dispatcher import FSMContext


@dp.callback_query_handler()
async def callback_filter(update : types.Message, state : FSMContext):
    if await db.is_user(update.from_user.id):
        pass

    elif await db.is_admin(update.from_user.id):
        pass

    else:
        pass


@dp.message_handler(commands='start')
async def start_filter(update : types.Message, state : FSMContext):
    if await db.is_user(update.from_user.id):
        pass

    elif await db.is_admin(update.from_user.id):
        pass

    else:
        pass



@dp.message_handler()
async def text_filter(update : types.Message, state : FSMContext):
    if await db.is_user(update.from_user.id):
        pass

    elif await db.is_admin(update.from_user.id):
        pass

    else:
        pass
