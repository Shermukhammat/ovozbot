from asyncpg.pool import PoolAcquireContext, Pool






async def creat_tables(pool : Pool):
    async with pool.acquire() as conn:
        conn : Pool
        # await conn.execute("DROP TABLE pre_voices;")
        await conn.execute("""CREATE TABLE IF NOT EXISTS users
                              (id BIGINT PRIMARY KEY, 
                               name TEXT, 
                               registered TIMESTAMP WITH TIME ZONE NOT NULL, 
                               status INTEGER, 
                               lang TEXT
                           );""")
        
        await conn.execute("""CREATE TABLE IF NOT EXISTS admins
                               (id BIGINT PRIMARY KEY, 
                               name TEXT, 
                               registered TIMESTAMP WITH TIME ZONE NOT NULL,
                               lang TEXT); """)
        
        await conn.execute("""CREATE TABLE IF NOT EXISTS voices
                           (id SERIAL PRIMARY KEY,
                           title TEXT,
                           tag TEXT,
                           url TEXT,
                           views BIGINT,
                           message_id BIGINT); """)
        
        await conn.execute("""CREATE TABLE IF NOT EXISTS pre_voices
                           (id SERIAL PRIMARY KEY,
                           user_id BIGINT,
                           title TEXT,
                           url TEXT,
                           username TEXT,
                           time TIMESTAMP WITH TIME ZONE NOT NULL,
                           message_id BIGINT); """)
        
        await conn.execute("""CREATE TABLE IF NOT EXISTS playlist
                           (user_id BIGINT,
                            voice_id BIGINT); """)
        await conn.execute("""CREATE UNIQUE INDEX IF NOT EXISTS unique_user_voice_idx ON playlist (user_id, voice_id);""")

        await conn.execute("""CREATE TABLE IF NOT EXISTS activity (id BIGINT UNIQUE); """)
        await conn.execute(""" CREATE TABLE IF NOT EXISTS subscription (
                           user_id BIGINT, 
                           chat_id TEXT, 
                           last_check TIMESTAMP WITH TIME ZONE NOT NULL, 
                           joined BOOLEAN DEFAULT FALSE,
                           UNIQUE (user_id, chat_id) 
                           ); """)
# self.user_id = user_id
#         self.chat_id = chat_id
#         self.join_requested = join_requested

#         if last_check:
        await conn.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")
        # await conn.execute("CREATE INDEX IF NOT EXISTS idx_musics_title ON musics USING gin (title gin_trgm_ops);")
        # await conn.execute("CREATE INDEX IF NOT EXISTS idx_musics_artist ON musics USING gin (artist gin_trgm_ops);")
        