from loader import dp, bot, db
from asyncio import sleep
from aiogram import types
from data import Subscribtion


@dp.chat_join_request_handler()
async def handle_join_request(join_request: types.ChatJoinRequest):
    chanel = db.CHANELS_DICT.get(f"{join_request.chat.id}")
    if chanel:
        sub = await db.get_subscription(join_request.from_user.id, f"{join_request.chat.id}")
        if sub:
            sub.joined = True
            await db.update_subscription(sub)

        sub = Subscribtion(join_request.from_user.id, f"{join_request.chat.id}", joined=True)
        await db.add_subscription(sub)

        count = await db.get_subscribed_users_count(f"{join_request.chat.id}")
        # print('chanel.user_count', chanel.user_count)
        # print('count: ', count)

        if chanel.user_count <= count:
            async with db.paramas_sem:
                if db.CHANELS_DICT.get(chanel.id) and chanel.id in db.CHANELS_DICT:
                    del db.CHANELS_DICT[chanel.id]
                    db.CHANELS.remove(chanel)
                    db.update_params()

                    await db.delete_subscription_chanel(f"{join_request.chat.id}")

                    for admin in await db.get_admins():
                        await bot.send_message(chat_id=admin.id, 
                                               text=f"📡 Kanal {chanel.name} odam qo'shish limitga yetdi \n👥 Odam qo'shildi: {count} \nHavola: {chanel.url}  \n❗️ Kanal majburiy obunadan olib tashlandi")


        if chanel.auto_join:    
            await sleep(10)
            await bot.approve_chat_join_request(chat_id=join_request.chat.id, user_id=join_request.from_user.id)


