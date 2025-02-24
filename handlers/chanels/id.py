from loader import dp, bot 
from asyncio import sleep
from aiogram import types



@dp.channel_post_handler(content_types=types.ContentType.PHOTO)
async def chanel_post(update : types.Message):
    # print(update)
    if update.photo:
        print(update.photo[-1].file_id)


@dp.channel_post_handler(content_types=types.ContentType.VIDEO)
async def chanel_post(update : types.Message):
    print(update)
    if update.video:
        print(update.video.file_id)


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

