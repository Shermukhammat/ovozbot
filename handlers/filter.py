from loader import bot, dp, db 
from aiogram import types
from aiogram.dispatcher import FSMContext
from .users.commands.start import user_register_hanlder, user_start_hanlder
from .users.inline.main import user_inline_search
import os
from uuid import uuid4


os.makedirs('data/voices', exist_ok=True)

# @dp.message_handler(content_types=types.ContentType.VOICE)
# async def vss(update : types.Message):
#     file = await bot.get_file(update.voice.file_id)
#     mimtype = file.file_path.split('.')[-1]
#     local_file_name = f"{uuid4().hex}.{mimtype}"

#     await file.download(destination_file = f'data/voices/{local_file_name}')
#     data = await bot.send_voice(chat_id=db.DATA_CHANEL_ID,
#                                 caption="test",
#                                 voice = open(f'data/voices/{local_file_name}', 'rb'))
#     print(data.voice.file_id)

    
    



@dp.inline_handler()
async def inline_filter(update : types.InlineQuery, state : FSMContext):
    user = await db.get_user(update.from_user.id)
    if user:
        await user_inline_search(update, user)

    elif await db.is_admin(update.from_user.id):
        pass

    else:
        pass


# @dp.callback_query_handler()
# async def callback_filter(update : types.Message, state : FSMContext):
#     if await db.is_user(update.from_user.id):
#         pass

#     elif await db.is_admin(update.from_user.id):
#         pass

#     else:
#         pass


@dp.message_handler(commands='start')
async def start_filter(update : types.Message, state : FSMContext):
    if await db.is_user(update.from_user.id):
        await user_start_hanlder(update)

    elif await db.is_admin(update.from_user.id):
        pass

    else:
        await user_register_hanlder(update)



@dp.message_handler()
async def text_filter(update : types.Message, state : FSMContext):
    if await db.is_user(update.from_user.id):
        pass

    elif await db.is_admin(update.from_user.id):
        pass

    else:
        pass
