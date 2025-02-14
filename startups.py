from aiogram import Dispatcher
from data import DataBase
import os, asyncio
from loader import db
from utilites import get_next_day_sec



async def on_startup(dp : Dispatcher):
    await db.init()
    db.bot = await dp.bot.get_me()
    asyncio.create_task(dayly_loop())


async def dayly_loop():
    while True:
        await asyncio.sleep(get_next_day_sec())
        await db.reset_dayly_tracks()
        

async def on_shutdown(dp : Dispatcher):
    await db.close()