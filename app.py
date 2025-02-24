from loader import dp
from aiogram import executor
from startups import on_shutdown, on_startup
from utilites import logger
import middlewares, handlers


if __name__ == '__main__':
    logger()
    executor.start_polling(dp, on_shutdown = on_shutdown, on_startup = on_startup, skip_updates = False)