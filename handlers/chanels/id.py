from loader import dp, bot 
from asyncio import sleep
from aiogram import types


@dp.channel_post_handler(regexp=r'/id')
async def chanel_post(update : types.Message):
    id = update.sender_chat.id
    message_data = await update.answer(f"id: `{id}`", parse_mode=types.ParseMode.MARKDOWN)

    await sleep(5)
    try:
        await update.delete()
        await message_data.delete()
    except:
        pass