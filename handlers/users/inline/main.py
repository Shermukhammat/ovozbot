from loader import bot, dp, db
from aiogram import types
from aiogram.dispatcher import FSMContext
from data import User, Voice
from uuid import uuid4



def sample_resolt():
    return types.InlineQueryResultVoice(id = uuid4().hex, 
                                        title='tes ovoz',
                                        voice_url = "AwACAgIAAyEGAASJ4vqHAAMsZ7BSa7M9n9mvBDKWxqVPZUBjvoEAAutgAAJIKYlJGkjReV5e9Ko2BA")

async def user_inline_search(update: types.InlineQuery, user: User):
    # print(update.query)
    if len(update.query) > 3:
        voices = await db.search_voices(update.query)
        if voices:
            await update.answer([inline_voice(voice) for voice in voices], cache_time = db.INLINE_CACHE_TIME)
        else:
            await update.answer([nofound("Hechnarsa topilmadi")], cache_time = db.INLINE_CACHE_TIME)

    else:
        voices = await db.get_top_voices()
        if voices:
            await update.answer([inline_voice(voice) for voice in voices], cache_time = db.INLINE_CACHE_TIME)
        else:
            await update.answer([nofound("Hozirda botda birortaham ovoz yoq")], cache_time = db.INLINE_CACHE_TIME)


input_content = types.InputTextMessageContent(f"/nofound")

def inline_voice(voice : Voice) -> types.InlineQueryResultVoice:
    return types.InlineQueryResultVoice(id = voice.str_id, voice_url=voice.url, title = voice.title)

def nofound(title : str | None = "Bunday janir mavjud emas", 
            description : str | None = None, 
            input_content : types.InputMessageContent | None = input_content):
    return types.InlineQueryResultArticle(id='nothingfoundid',
                                    title=title,
                                    description = description,
                                    input_message_content = input_content,
                                    thumb_url=db.NO_FOUND_URL)