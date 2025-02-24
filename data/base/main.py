import asyncpg, asyncio
from asyncpg import Pool, Connection
from .tables import creat_tables
from .params import ParamsDB
from .admins import Admin, AdminsDB
from aiogram.types import User as AiogramUser
from .users import User, UserStatus, UsersDB
from .activity import ActivityTracker
from .statistic import Statistic
from .voices import VoicesDb
from .subscription import SubscribtionDB


class DataBase(ParamsDB, UsersDB,AdminsDB, ActivityTracker, Statistic, VoicesDb, SubscribtionDB):
    def __init__(self, config_file_path : str) -> None:
        UsersDB.__init__(self, ttl = 30)
        AdminsDB.__init__(self, ttl = 30)
        VoicesDb.__init__(self, ttl = 30)
        ActivityTracker.__init__(self)
        Statistic.__init__(self)
        SubscribtionDB.__init__(self, ttl = 30)
        ParamsDB.__init__(self, config_file_path)
        self.pool : Pool = None
        self.bot : AiogramUser = None


    async def init(self):
        self.pool : Pool = await asyncpg.create_pool(user=self.config.user, 
                                         password=self.config.pasword,
                                         database=self.config.database, 
                                         host=self.config.host,
                                         port = self.config.port)
        await creat_tables(self.pool)
    

    async def close(self):
        await self.pool.close()



