from asyncpg.pool import PoolAcquireContext, Pool
from datetime import datetime
from aiocache import SimpleMemoryCache
from pytz import timezone

tz_tashkent = timezone('Asia/Tashkent')

class Voice:
    def __init__(self,
                 id : int = None, 
                 title : str = None,
                 tag : str = None,
                 url : str = None,
                 views : int = 0,
                 in_playlist : int = 0,
                 message_id : int = None ) -> None:
        self.id = id
        self.title = title
        self.tag = tag
        self.url = url
        self.views = views
        self.message_id = message_id
        self.in_playlist = in_playlist
        self.tag = self.title

    @property
    def str_id(self) -> str:
        return str(self.id)

    def __str__(self) -> str:
        return f"Voice(id = {self.id}, title = '{self.title}', tag = '{self.tag}', url = '{self.url}', message_id = {self.message_id})"

class PreVoice:
    def __init__(self,
                 id : int = None,
                 url : str = None,
                 user_id : int = None,
                 time : datetime = None,
                 title : str = None,
                 username : str = None,
                 message_id : int = None) -> None:
        self.id = id
        self.url = url
        self.title = title
        self.user_id = user_id
        self.message_id = message_id
        self.username = username
        self.tag = title
        
        if time:
            self.time = time
        else:
            self.time = datetime.now(tz_tashkent)

    @property
    def readble_time(self) -> str: 
        return self.time.strftime('%Y.%m.%d %H:%M')

    @property
    def str_id(self) -> str:
        return str(self.id)

    def __str__(self) -> str:
        return f"PreVoice(id = {self.id}, user_id = '{self.user_id}', url = '{self.url}', message_id = {self.message_id})"





class VoicesDb:
    def __init__(self, ttl : int = 30):
        self.voices_cache = SimpleMemoryCache(ttl = ttl)
        self.playlist_cache = SimpleMemoryCache(ttl = ttl)
        self.pre_voices_cache = SimpleMemoryCache(ttl = ttl)
        self.pool : Pool = None
        self.PINED_VOICES : list[int] = []
        
    
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


    async def get_playlist(self, user_id) -> list[int]:
        playlist = await self.playlist_cache.get(user_id)
        if playlist:
            return playlist
        
        async with self.pool.acquire() as conn:
            conn : Pool
            playlist = [row['voice_id'] for row in await conn.fetch(" SELECT voice_id FROM playlist WHERE user_id = $1 ORDER BY ctid DESC; ", user_id)]
            await self.playlist_cache.set(user_id, playlist)

            return playlist

    async def add_voice_to_playlist(self, user_id : int, voice_id : int):
        playlist : list[int] = await self.playlist_cache.get(user_id)
        if playlist:
            playlist.insert(0, voice_id)
            await self.playlist_cache.set(user_id, playlist)

        async with self.pool.acquire() as conn:
            conn : Pool
            await conn.execute("INSERT INTO playlist (user_id, voice_id) VALUES($1, $2)", user_id, voice_id)

    async def remove_voice_from_playlist(self, user_id : int, voice_id : int):
        playlist : list[int] = await self.playlist_cache.get(user_id)
        if playlist:
            playlist.remove(voice_id)
            await self.playlist_cache.set(user_id, playlist)

        async with self.pool.acquire() as conn:
            conn : Pool
            await conn.execute("DELETE FROM playlist WHERE user_id = $1 AND voice_id = $2", user_id, voice_id)
    
    async def get_top_voices(self) -> list[Voice]:
        voices : list = await self.voices_cache.get('top', [])
        if voices:
            return voices
        
        async with self.pool.acquire() as conn:
            conn : Pool
            for row in await conn.fetch(""" SELECT v.id, v.title, v.tag, v.url, v.views, v.message_id, COUNT(p.voice_id) AS usage_count
        FROM voices v
        JOIN playlist p ON v.id = p.voice_id
        GROUP BY v.id
        ORDER BY usage_count DESC
        LIMIT 47; """):
                voices.append(Voice(id = row['id'],
                                    tag = row['tag'],
                                    url = row['url'],
                                    views = row['views'],
                                    in_playlist = row['usage_count'],
                                    message_id = row['message_id'],
                                    title=row['title']))

            await self.voices_cache.set('top', voices, ttl = 200)
            return voices

    async def get_pined_voices(self, offset : int | None = 0, limit : int | None = 50) -> list[Voice]:
        pined : list = await self.voices_cache.get(f'pined{offset}', [])
        if pined:
            return pined
        
        if len(self.PINED_VOICES) > offset:
            for index, id in enumerate(self.PINED_VOICES[offset:]):
                if index < limit:
                    voice = await self.get_voice(id)
                    if voice:
                        pined.append(voice)
                else:
                    break

            await self.voices_cache.set(f'pined{offset}', pined, ttl = 200)
            return pined
        
        return []

    async def get_lates_voices(self, limit : int | None = 45, offset : int | None = 0) -> list[Voice]: 
        lates : list = await self.voices_cache.get(f'lates{offset}')
        if lates:
            return lates
        
        query = "SELECT id, title, tag, url, message_id, views FROM voices ORDER BY id DESC OFFSET $1 LIMIT $2; "
        async with self.pool.acquire() as conn:
            conn : Pool
            lates = [Voice(id=row['id'], title=row['title'], tag=row['tag'], url=row['url'], message_id=row['message_id'], views=row['views']) for row in await conn.fetch(query, offset, limit)]
            
            await self.voices_cache.set(f'lates{offset}', lates)
            return lates
    
    async def add_pre_voice(self, voice : PreVoice) -> bool:
        async with self.pool.acquire() as conn:
            conn : Pool
            row = await conn.fetchrow(""" INSERT INTO pre_voices (user_id, url, message_id, time, username, title) VALUES($1, $2, $3, $4, $5, $6) RETURNING id;""", voice.user_id, voice.url, voice.message_id, voice.time, voice.username, voice.title)
            if row:
                voice.id = row[0]
                await self.pre_voices_cache.set(voice.id, voice)
                return True
            return False
    
    async def delete_pre_voice(self, id : int):
        await self.pre_voices_cache.delete(id)
        async with self.pool.acquire() as conn:
            conn : Pool
            await conn.execute(""" DELETE FROM pre_voices WHERE id = $1;""", id)

    async def get_pre_voice(self, id : int) -> PreVoice:
        await self.pre_voices_cache.delete(id)
        async with self.pool.acquire() as conn:
            conn : Pool
            row = await conn.fetchrow("SELECT time AT TIME ZONE 'Asia/Tashkent', username, id, user_id, url, message_id, title FROM pre_voices WHERE id = $1;", id)
            if row:
                voice = PreVoice(id = row['id'], url = row['url'], user_id=row['user_id'], message_id=row['message_id'], username=row['username'], time=row[0], title=row['title'])
                await self.pre_voices_cache.set(id, voice)
                return voice
            
    async def get_pre_voices(self, offset : int | None = 0, limit : int | None = 10) -> list[PreVoice]:
        voices : list[PreVoice] = await self.pre_voices_cache.get(f'pre{offset}', [])
        if voices:
            return voices
        
        async with self.pool.acquire() as conn:
            conn : Pool
            for row in  await conn.fetch("SELECT time AT TIME ZONE 'Asia/Tashkent', username, id, user_id, url, message_id, title FROM pre_voices ORDER BY id DESC LIMIT $1 OFFSET $2;", limit, offset):
                voices.append(PreVoice(id = row['id'], url = row['url'], user_id=row['user_id'], message_id=row['message_id'], username=row['username'], time=row[0], title=row['title']))
        
        await self.pre_voices_cache.set(f'pre{offset}', voices)
        return voices

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