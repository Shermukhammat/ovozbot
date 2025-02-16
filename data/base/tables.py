from asyncpg.pool import PoolAcquireContext, Pool






async def creat_tables(pool : Pool):
    async with pool.acquire() as conn:
        conn : Pool
        # await conn.execute("DROP TABLE voices;")
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
                               registered TIMESTAMP,
                               lang TEXT); """)
        
        await conn.execute("""CREATE TABLE IF NOT EXISTS voices
                           (id SERIAL PRIMARY KEY,
                           title TEXT,
                           tag TEXT,
                           url TEXT,
                           views BIGINT,
                           message_id BIGINT); """)
        

        await conn.execute("""CREATE TABLE IF NOT EXISTS activity (id BIGINT UNIQUE); """)

        await conn.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")
        # await conn.execute("CREATE INDEX IF NOT EXISTS idx_musics_title ON musics USING gin (title gin_trgm_ops);")
        # await conn.execute("CREATE INDEX IF NOT EXISTS idx_musics_artist ON musics USING gin (artist gin_trgm_ops);")
        