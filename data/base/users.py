from asyncpg.pool import PoolAcquireContext, Pool
from datetime import datetime
from aiocache import SimpleMemoryCache
from datetime import datetime, timezone as d_timezone
from pytz import timezone
from aiogram.utils.markdown import escape_md

tz_tashkent = timezone('Asia/Tashkent')

class UserStatus:
    active = 1
    blocked = 2


class User:
    def __init__(self,
                 id : int = None, 
                 name : str = None,
                 lang : str = 'uz',
                 registered : datetime = None,
                 status : int = UserStatus.active
                 ) -> None:
        self.id = id
        self.lang = lang
        self.name = name
        self.status = status

        if registered:
            self.registered = registered
        else:
            self.registered = datetime.now(tz_tashkent)


    @property
    def registred_readble(self) -> str: 
        return f"{self.registered.year}.{self.registered.month}.{self.registered.day} {self.registered.hour}:{self.registered.second}"

    @property
    def is_active(self) -> bool:
        return self.status == UserStatus.active
    
    @property
    def safe_name(self) -> str:
        return escape_md(self.name)

class UsersDB:
    def __init__(self, ttl = 20) -> None: 
        self.users_cache  = SimpleMemoryCache(ttl = ttl)
        self.pool : Pool = None
    
    async def is_user(self, id : int) -> bool:
        if await self.users_cache.get(id):
            return True
        
        user = await get_user_from_db(self.pool, id)
        if user:
            await self.users_cache.set(id, user)
            return True


    async def register_user(self, user : User):
        await registr_user_to_db(self.pool, user)
        await self.users_cache.set(user.id, user)
        
    
    async def get_user(self, id : int) -> User:
        user = await self.users_cache.get(id)
        if user:
            return user
        
        user = await get_user_from_db(self.pool, id)
        if user:
            await self.users_cache.set(user.id, user)
            return user
        
    
    async def remove_user(self, id : int):
        await self.users_cache.delete(id)
        await delete_user_from_db(self.pool, id)

    async def update_user(self, id : int, **kwargs):
        await update_user_data_from_db(self.pool, id, **kwargs)
        user = await get_user_from_db(self.pool, id)
        if user:
            await self.users_cache.set(id, user)
    
    async def get_useres(self) -> list[User]:
        async with self.pool.acquire() as conn:
            conn : Pool
            useres = []
            rows = await conn.fetch("""SELECT registered, status, name, lang, id FROM users;""")
            for row in rows:
                useres.append(User(id = row['id'], registered = row['registered'], status = row['status'], name = row['name'], lang = row['lang']))
            return useres

async def update_user_data_from_db(pool : Pool, id : int, **kwargs):
    async with pool.acquire() as conn:
        conn : Pool
        for key, value in kwargs.items():
            await conn.execute(f""" UPDATE users SET {key} = $1 WHERE id = $2""", value, id)

async def delete_user_from_db(pool : Pool, id : int):
    async with pool.acquire() as conn:
        conn : Pool
        await conn.execute(""" DELETE FROM users WHERE id = $1""", id)
        await conn.execute(""" DELETE FROM activity WHERE id = $1""", id)


async def registr_user_to_db(pool : Pool, user : User):
    async with pool.acquire() as conn:
        conn : Pool
        query = """ INSERT INTO users (id, registered, status, name, lang) VALUES($1, $2, $3, $4, $5); """
        values = (user.id, user.registered, user.status, user.name, user.lang)
        await conn.execute(query, *values)
        await conn.execute(""" INSERT INTO activity (id) VALUES ($1) ON CONFLICT (id) DO NOTHING; """, user.id)


async def get_user_from_db(pool : Pool, id : int) -> User:
    async with pool.acquire() as conn:
        conn : Pool
        row = await conn.fetchrow("""SELECT registered AT TIME ZONE 'Asia/Tashkent', status, name, lang FROM users WHERE id = $1""", id)
        if row:
            await conn.execute(""" INSERT INTO activity (id) VALUES ($1) ON CONFLICT (id) DO NOTHING; """, id)
            return User(id = id, 
                    registered=row[0],
                    status=row[1],
                    name=row[2],
                    lang=row[3])