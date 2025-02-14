from aiogram import Bot, Dispatcher
from data import DataBase
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from asyncio import Semaphore


db = DataBase('data/config.yaml')
bot = Bot(db.TOKEN)
dp = Dispatcher(bot, storage = MemoryStorage())

register_sema = Semaphore()