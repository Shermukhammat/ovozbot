from aiogram import types, Bot
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from loader import bot, db
from data import Chanel, Subscribtion
from aiogram.utils.exceptions import ChatAdminRequired, ChatNotFound
from uuid import uuid4



async def subscribed(sub : Subscribtion) -> bool:
    try:
        member  = await bot.get_chat_member(chat_id = sub.chat_id, user_id = sub.user_id)
        if member and member.status != 'left':
            return True
        return False
    except:
        return False


async def check_subscription(user_id : int, chanels : list[Chanel]) -> list[InlineKeyboardButton]:
    chanels_button = []
    for chanel in chanels:
        if chanel.request_join:
            pass

        else:
            sub = await db.get_subscription(user_id, chanel.id)
            if sub:
                if sub.joined:
                    if sub.should_check(minutes = 15):
                        sub.upate_last_check()
                        if await subscribed(sub):
                            await db.update_subscription(sub)
                        else:
                            sub.joined = False
                            await db.update_subscription(sub)
                            chanels_button.append([InlineKeyboardButton(chanel.name, url=chanel.url)])
                
                elif await subscribed(sub):
                    sub.joined = True
                    sub.upate_last_check()
                    await db.update_subscription(sub)

                else:
                    chanels_button.append([InlineKeyboardButton(chanel.name, url=chanel.url)])
                
        
            else:
                sub = Subscribtion(user_id, chanel.id)
                if await subscribed(sub):
                    sub.joined = True
                    await db.add_subscription(sub)
                else:
                    await db.add_subscription(sub)
                    chanels_button.append([InlineKeyboardButton(chanel.name, url=chanel.url)])
    
    return chanels_button


async def message_checking(update : types.Message, chanels : list[Chanel]):
    if update.via_bot:
        raise CancelHandler()
    
    chanels_button = await check_subscription(update.from_user.id, chanels)
    if chanels_button:
        chanels_button.append([InlineKeyboardButton("✅ Tekshirish", callback_data='check_sub')])
        await update.answer("❌ Botdan foydalanish uchun quydagi kanallarga obuna bo'lishingiz kerak",
                            reply_markup=InlineKeyboardMarkup(inline_keyboard=chanels_button)) 
        raise CancelHandler()

async def callback_checking(update : types.CallbackQuery, chanels : list[Chanel]):
    chanels_button = await check_subscription(update.from_user.id, chanels)

    if chanels_button:
        if update.data == 'check_sub':
            await update.answer("❌ Barcha kanallarga obuna bo'lmadingiz", show_alert=True, cache_time=5)
            raise CancelHandler()
        
        chanels_button.append([InlineKeyboardButton("✅ Tekshirish", callback_data='check_sub')])
        if update.message:
            await update.message.reply("❌ Botdan foydalanish uchun quydagi kanallarga obuna bo'lishingiz kerak",
                                   reply_markup=InlineKeyboardMarkup(inline_keyboard=chanels_button))
        else:
            await bot.send_message(chat_id=update.from_user.id,
                                   text = "❌ Botdan foydalanish uchun quydagi kanallarga obuna bo'lishingiz kerak",
                                   reply_markup = InlineKeyboardMarkup(inline_keyboard=chanels_button))

        raise CancelHandler()


async def inline_checking(update : types.InlineQuery, chanels : list[Chanel]):
    if await db.is_user(update.from_user.id) or await db.is_admin(update.from_user.id) or update.chat_type == 'sender':
        chanels_button = await check_subscription(update.from_user.id, chanels)
        if chanels_button:
            chanels_button.append([InlineKeyboardButton("🔍 Ovoz izlash", switch_inline_query_current_chat = "")])
            await update.answer([types.InlineQueryResultArticle(id = uuid4().hex,
                                                                thumb_url=db.NO_FOUND_URL,
                                                                reply_markup = InlineKeyboardMarkup(inline_keyboard=chanels_button),
                                                                description = "➡️ Buyerga bosing",
                                                                input_message_content=types.InputTextMessageContent("👇 Quydagi kanallarga obuna bo'ling"),
                                                                title = "❌ Obuna bo'lishingiz kerak")],
                                                                cache_time=5, 
                                                                is_personal = True)
            raise CancelHandler()

    
class ForcedSubscribtion(BaseMiddleware):
    async def on_pre_process_update(self, update : types.Update,  data: dict):
        chanels = db.CHANELS
        if chanels:
            if update.message:
                await message_checking(update.message, chanels)
            
            elif update.callback_query:
                await callback_checking(update.callback_query, chanels)
            
            elif update.inline_query:
                await inline_checking(update.inline_query, chanels)
            
            