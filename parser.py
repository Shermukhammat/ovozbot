from pyrogram import Client, types
import asyncio
from data import DataBase, Voice



async def main():
    db = DataBase('data/config.yaml')
    last = db.params_data.get('last', 1)
    await db.init()

    async with Client("sher", db.API_ID, db.API_HASH) as app:
        await app.send_message('@ovozqaniibot', 'Kulgili ovozlar😆')
        await asyncio.sleep(2)
        async for message in app.get_chat_history('@ovozqaniibot', limit = 1):
            message : types.Message
            print(message.reply_markup)

        return
        for n in range(last, 300):
            message = await app.send_message('@ovozqanibot', f"/{n}")
            await asyncio.sleep(15)
        
            message = await get_last_message(app)
            if message.voice and message.caption:
                file = await app.download_media(message.voice.file_id, in_memory = True)
                message_data = await app.send_voice('@dfdfdffddfdds', file)
                if isinstance(message_data, types.Message):
                    title = parse(message.caption, 'Название')
                    print(n, 'title:', title)
                    if title:
                        tag = parse_tag(message.caption)
                        vs = Voice(title=title, tag=tag, url=message_data.voice.file_id, message_id=message_data.id)
                        await db.add_voice(vs)
                    # print(message.voice.file_id)
                    # print(message_data.id)

            db.params_data['last'] = n 
            db.update_params()

    await db.close()  

async def get_last_message(app : Client) -> types.Message:
    async for message in app.get_chat_history('@ovozqanibot', limit = 1):
        return message 

def parse(caption: str, key : str) -> str:
    for row in caption.split('\n'):
        args = row.split(':', maxsplit=1)
        if len(args) == 2:
            if args[0].strip() == key and len(args[1]) > 2:
                return args[1]
                

def parse_tag(caption: str) -> str:
    tag = parse(caption, 'Название')
    tag += ', '
    for key in ['Исполнитель', 'Название шоу', 'Теги']:
        data = parse(caption, key)
        if data:
            tag += data
    return tag

asyncio.run(main())
