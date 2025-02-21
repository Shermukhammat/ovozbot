from data import DataBase, Voice, PreVoice
import asyncio



async def main():
    db = DataBase('data/config.yaml')
    await db.init()

    # vs = Voice(title="Maqtov yorliq beringlar", tag="Maqtov yorliq beringlar, milyon", url="AwACAgIAAyEGAASJ4vqHAAMvZ7Bh6OIt3IjvKlooWIirmEnxe_4AApdlAALNUolJC1OqZNGAk9Q2BA", message_id = 47)
    # print(await db.add_voice(vs))
    for n in range(1, 500):
        print(n)
        # await db.add_voice(Voice(url='AwACAgIAAyEGAASJ4vqHAAOwZ7XlecmFC4BuvvWB-VsEK0JeFQUAAlFmAAI1dLBJs8u8QpFhUS82BA',
        #                                 title=f'Test ovoz {n}',
        #                                 tag=f"test teg {n}",
        #                                 message_id=176))
    # print(await db.get_top_voices())


asyncio.run(main())