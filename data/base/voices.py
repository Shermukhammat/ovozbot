from asyncpg.pool import PoolAcquireContext, Pool
from datetime import datetime
from aiocache import SimpleMemoryCache


class Voice:
    def __init__(self,
                 id : int = None, 
                 title : str = None,
                 tag : str = None,
                 url : str = None,
                 views : int = 0,
                 message_id : int = None ) -> None:
        self.id = id
        self.title = title
        self.tag = tag
        self.url = url
        self.views = views
        self.message_id = message_id

    @property
    def str_id(self) -> str:
        return str(self.id)

    def __str__(self) -> str:
        return f"Voice(id = {self.id}, title = '{self.title}', tag = '{self.tag}', url = '{self.url}', message_id = {self.message_id})"





class VoicesDb:
    def __init__(self, ttl : int = 30):
        self.voices_cache = SimpleMemoryCache(ttl = ttl)
        self.pool : Pool = None
        
    
    async def add_voice(self, voice : Voice) -> int:
        id = await add_voice_to_db(self.pool, voice)
        if id:
            voice.id = id
            await self.voices_cache.set(id, voice)
            return id
        
    async def get_voice(self, id : int) -> Voice:
        voice = await self.voices_cache.get(id)
        if voice:
            return voice
        
        voice = await get_voice_from_db(self.pool, id)
        if voice:
            await self.voices_cache.set(id, voice)
            return voice
    
    async def remove_voice(self, id : int):
        await self.voices_cache.delete(id)
        async with self.pool.acquire() as conn:
            conn : Pool
            await conn.execute(""" DELETE FROM voices WHERE id = $1""", id)


    async def search_voices(self, query : str, limit : int = 20) -> list[Voice]:
        sql_query = """SELECT id, title, tag, url, message_id, views 
        FROM voices
        WHERE SIMILARITY(tag, $1) > 0.2
        ORDER BY SIMILARITY(tag, $2) DESC 
        LIMIT $3; """
        async with self.pool.acquire() as conn:
            conn : Pool
            return [Voice(id=row['id'], title=row['title'], tag=row['tag'], url=row['url'], message_id=row['message_id'], views=row['views']) for row in await conn.fetch(sql_query, query, query, limit)]


    async def get_top_voices(self, limit : int = 20) -> list[Voice]:
        top = await self.voices_cache.get('top')
        if top:
            return top
        
        query = "SELECT id, title, tag, url, message_id, views FROM voices ORDER BY views DESC LIMIT $1; "
        async with self.pool.acquire() as conn:
            conn : Pool
            top = [Voice(id=row['id'], title=row['title'], tag=row['tag'], url=row['url'], message_id=row['message_id'], views=row['views']) for row in await conn.fetch(query, limit)]
            
            await self.voices_cache.set('top', top)
            return top


async def add_voice_to_db(pool : Pool, voice : Voice) -> int:
    async with pool.acquire() as conn:
        conn : Pool
        query = """ INSERT INTO voices (title, tag, url, message_id, views) VALUES($1, $2, $3, $4, $5) RETURNING id; """
        values = (voice.title, voice.tag, voice.url, voice.message_id, voice.views)
        row = await conn.fetchrow(query, *values)
        if row:
            return row[0]
        
async def get_voice_from_db(pool: Pool, id: int) -> Voice:
    async with pool.acquire() as conn:
        conn: Pool
        query = """ SELECT id, title, tag, url, message_id, views FROM voices WHERE id = $1; """
        row = await conn.fetchrow(query, id)
        if row:
            return Voice(
                id=row['id'],
                title=row['title'],
                tag=row['tag'],
                url=row['url'],
                message_id=row['message_id'],
                views=row['views'])