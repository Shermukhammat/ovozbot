from asyncpg.pool import PoolAcquireContext, Pool
from datetime import datetime, timedelta
from aiocache import SimpleMemoryCache
from datetime import datetime, timezone as d_timezone
from pytz import timezone
from aiogram.utils.markdown import escape_md


tz_tashkent = timezone('Asia/Tashkent')

class Subscribtion:
    def __init__(self, user_id : int, chat_id : str, last_check : datetime = None, joined : bool = False):
        self.user_id = user_id
        self.chat_id = chat_id
        self.joined = joined

        if last_check:
            self.last_check = last_check.astimezone(tz_tashkent)
        else:
            self.last_check = datetime.now(tz_tashkent) 

    def should_check(self, minutes: int = 5) -> bool:
        now = datetime.now(tz_tashkent)
        check_time = self.last_check + timedelta(minutes=minutes)
        return now >= check_time
    
    def upate_last_check(self):
        self.last_check = datetime.now(tz_tashkent) 


class SubscribtionDB:
    def __init__(self, ttl = 30) -> None: 
        self.subscription_cache  = SimpleMemoryCache(ttl = ttl)
        self.pool : Pool = None

    async def get_subscription(self, user_id: int, chat_id : str) -> Subscribtion:
        sub = await self.subscription_cache.get(f"{user_id}.{chat_id}")
        if sub:
            return sub
        
        async with self.pool.acquire() as conn:
            conn: Pool
            row = await conn.fetchrow("SELECT last_check AT TIME ZONE 'Asia/Tashkent' as last_check, joined FROM subscription WHERE user_id = $1 AND chat_id = $2;", user_id, chat_id)
            if row:
                sub = Subscribtion(
                    user_id=user_id,
                    chat_id=chat_id,
                    last_check=row['last_check'],
                    joined=row['joined']
                    )
                await self.subscription_cache.set(f"{user_id}.{chat_id}", sub)
                return sub

    async def add_subscription(self, sub: Subscribtion):
        await self.subscription_cache.set(f"{sub.user_id}.{sub.chat_id}", sub)
        async with self.pool.acquire() as conn:
            conn : Pool
            await conn.execute("""INSERT INTO subscription (user_id, chat_id, last_check, joined)
                               VALUES ($1, $2, $3, $4)
                               ON CONFLICT (user_id, chat_id) DO NOTHING;""",
                               sub.user_id, sub.chat_id, sub.last_check, sub.joined)
    

    async def update_subscription(self, sub: Subscribtion):
        await self.subscription_cache.set(f"{sub.user_id}.{sub.chat_id}", sub)
        async with self.pool.acquire() as conn:
            conn: Pool
            await conn.execute(
                "UPDATE subscription SET joined = $1, last_check = $2 WHERE user_id = $3 AND chat_id = $4;",
                sub.joined, sub.last_check, sub.user_id, sub.chat_id
            )

    async def delete_subscription_chanel(self, chat_id: str):
        async with self.pool.acquire() as conn:
            conn: Pool
            await conn.execute("DELETE FROM subscription WHERE chat_id = $1", chat_id)


    async def get_subscribed_users_count(self, chat_id: str) -> int:
        cache_key = f"count{chat_id}"
        count = await self.subscription_cache.get(cache_key)
        if count is not None:
            return count

        async with self.pool.acquire() as conn:
            conn: Pool
            row = await conn.fetchrow("SELECT COUNT(chat_id) FROM subscription WHERE chat_id = $1 AND joined = TRUE ;", chat_id)
            if row:
                count = row[0]
                await self.subscription_cache.set(cache_key, count, ttl = 10)
                return count

        return 0