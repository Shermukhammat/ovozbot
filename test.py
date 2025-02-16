from data import DataBase, Voice
import asyncio



async def main():
    db = DataBase('data/config.yaml')
    await db.init()

    # vs = Voice(title="Maqtov yorliq beringlar", tag="Maqtov yorliq beringlar, milyon", url="AwACAgIAAyEGAASJ4vqHAAMvZ7Bh6OIt3IjvKlooWIirmEnxe_4AApdlAALNUolJC1OqZNGAk9Q2BA", message_id = 47)
    # print(await db.add_voice(vs))
    print(await db.get_top_voices())


asyncio.run(main())