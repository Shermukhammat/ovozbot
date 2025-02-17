from asyncpg.pool import PoolAcquireContext, Pool
from datetime import datetime
from aiocache import SimpleMemoryCache
from datetime import datetime
from pytz import timezone
from aiogram.utils.markdown import escape_md


tz_tashkent = timezone('Asia/Tashkent')


class Admin:
    def __init__(self,
                 id : int = None, 
                 name : str = None,
                 lang : str = 'uz',
                 registered : datetime = None
                 ) -> None:
        self.id = id
        self.lang = lang
        self.name = name

        if registered:
            self.registered = registered
        else:
            self.registered = datetime.now(tz_tashkent)

    @property
    def registred_readble(self) -> str:
        return self.registered.strftime('%Y-%m-%d %H:%M')

    def __str__(self) -> str:
        return f"Admin(id = {self.id}, name = '{self.name}', registered = '{self.registred_readble}')"

    @property
    def safe_name(self) -> str:
        return escape_md(self.name)

class AdminsDB:
    def __init__(self, ttl : int = 20) -> None:
        self.admins_cache = SimpleMemoryCache(ttl = ttl)
        self.pool : Pool = None
    
    async def is_admin(self, id : int) -> bool:
        if await self.admins_cache.get(id):
            return True
        
        admin = await get_admin_from_db(self.pool, id)
        if admin:
            await self.admins_cache.set(id, admin)
            return True


    async def register_admin(self, admin : Admin):
        await registr_admin_to_db(self.pool, admin)
        await self.admins_cache.set(admin.id, admin)
        
    
    async def get_admins(self) -> list[Admin]:
        return await get_admins_from_db(self.pool)

    async def get_admin(self, id : int) -> Admin:
        admin = await self.admins_cache.get(id)
        if admin:
            return admin
        
        admin = await get_admin_from_db(self.pool, id)
        if admin:
            await self.admins_cache.set(admin.id, admin)
            return admin
        
    
    async def remove_admin(self, id : int):
        await self.admins_cache.delete(id)
        await delete_admin_from_db(self.pool, id)

    async def update_admin(self, id : int, **kwargs):
        await update_admin_data_from_db(self.pool, id, **kwargs)
        admin = await get_admin_from_db(self.pool, id)
        if admin:
            await self.admins_cache.set(id, admin)


async def update_admin_data_from_db(pool : Pool, id : int, **kwargs):
    async with pool.acquire() as conn:
        conn : Pool
        for key, value in kwargs.items():
            await conn.execute(f""" UPDATE admins SET {key} = $1 WHERE id = $2""", value, id)

async def delete_admin_from_db(pool : Pool, id : int):
    async with pool.acquire() as conn:
        conn : Pool
        await conn.execute(""" DELETE FROM admins WHERE id = $1""", id)


async def registr_admin_to_db(pool : Pool, admin : Admin):
    async with pool.acquire() as conn:
        conn : Pool
        query = """ INSERT INTO admins (id, registered, name, lang) VALUES($1, $2, $3, $4); """
        values = (admin.id, admin.registered, admin.name, admin.lang)
        await conn.execute(query, *values)


async def get_admin_from_db(pool : Pool, id : int) -> Admin:
    async with pool.acquire() as conn:
        conn : Pool
        row = await conn.fetchrow("""SELECT registered AT TIME ZONE 'Asia/Tashkent', name, lang FROM admins WHERE id = $1;""", id)
        if row:
            return Admin(id = id, 
                    registered=row[0],
                    name=row['name'],
                    lang=row['lang'])
        

async def get_admins_from_db(pool : Pool) -> list[Admin]:
    resolt = []
    async with pool.acquire() as conn:
        conn : Pool
        for row in await conn.fetch("""SELECT id, registered AT TIME ZONE 'Asia/Tashkent', name, lang FROM admins;"""):
            resolt.append(Admin(id = row['id'], 
                    registered=row['registered'],
                    name=row['name'],
                    lang=row['lang']))
    return resolt