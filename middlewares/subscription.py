from aiogram import types, Bot
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from loader import bot, db
from data import Chanel, Subscribtion
from aiogram.utils.exceptions import ChatAdminRequired, ChatNotFound


async def subscribed(sub : Subscribtion) -> bool:
    try:
        member  = await bot.get_chat_member(chat_id = sub.chat_id, user_id = sub.user_id)
        if member and member.status != 'left':
            return True
        return False
    except:
        return False


async def message_checking(update : types.Message, chanels : list[Chanel]):
    chanels_button = []
    for chanel in chanels:
        if chanel.request_join:
            pass

        else:
            sub = await db.get_subscription(update.from_user.id, chanel.id)
            if sub:
                if sub.joined:
                    if sub.should_check(minutes = 5):
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
                sub = Subscribtion(update.from_user.id, chanel.id)
                if await subscribed(sub):
                    sub.joined = True
                    await db.add_subscription(sub)
                else:
                    await db.add_subscription(sub)
                    chanels_button.append([InlineKeyboardButton(chanel.name, url=chanel.url)])

    if chanels_button:
        await update.answer("Quydagi kanallarga obuna bo'ling",
                            reply_markup=InlineKeyboardMarkup(inline_keyboard=chanels_button)) 
        raise CancelHandler()     


class ForcedSubscribtion(BaseMiddleware):
    async def on_pre_process_update(self, update : types.Update,  data: dict):
        chanels = db.CHANELS
        if chanels:
            if update.message:
                await message_checking(update.message, chanels)