import asyncio
from os.path import isfile
from sqlite3 import connect
from typing import Any, Dict, List, Tuple, Optional, TYPE_CHECKING
import os
import typing
import dotenv

dotenv.load_dotenv()

PG_USER = os.getenv("POSTGRES_USER")
PG_PASSWORD = os.getenv("POSTGRES_PASSWORD")
PG_DB_NAME = os.getenv("POSTGRES_DB_NAME")
PG_HOST = os.getenv("POSTGRES_HOST")
PG_PORT = os.getenv("POSTGRES_PORT")

DB_PATH = "data/db/database.db"
BUILD_PATH="data/db/build.sql"

class DBCache(dict):   # Implementation of an auto populating dict cache
    def __init__(self, db_query: str, limit: int = 100):
        self.db_query = db_query
        self.limit = limit
        self.record_names = (
            self.db_query[
                db_query.index("SELECT") + len("SELECT") : db_query.index("FROM")
            ]
            .strip()
            .split(",")
        )
        return super().__init__()
    
    
    async def __getitem__(self, key: int)->List[str]|Tuple[List[str],List[str]]: #Return info based on Guild ID
        if key in self:
            return super().get(key)#type:ignore
        else:
            if len(self) >= self.limit:
                self.pop(tuple(self.keys())[0])
            async with pool.acquire() as conn:
                assert isinstance(conn, Connection)
                record = (await conn.fetch(self.db_query, key)) # Record will always be a sequence with one element
                if record is None:
                    await conn.execute(f"INSERT INTO GuildData (guildid) VALUES ({key})")
                    record=(await conn.fetch(self.db_query, key))[0]
                else:
                    record=record[0]
                return_element = tuple([
                    record[record_name] for record_name in self.record_names
                ])  # If there are two record_names then return_element will contain both of them
                if len(return_element) == 1:
                    self[key] = return_element[0]
                    return return_element[0]
                else:
                    self[key] = return_element
                    return return_element


import asyncpg
from asyncpg import Pool, Connection

alias_cache= DBCache("SELECT aliastext,aliassprites FROM GuildData WHERE GuildID=$1")
prefix_cache = DBCache("SELECT prefixes FROM GuildData WHERE GuildID=$1", limit=250)
pool:Pool


async def setup_database():
    global pool
    if TYPE_CHECKING:
        assert isinstance(pool,Pool)
    else:
        pool = await asyncpg.create_pool(
        f"postgres://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB_NAME}"
    )
    await pool.execute(open(BUILD_PATH,"r").read()) #Create database table if not exists
    return pool

async def insert_new_prefix(guild_id:int,new_prefix:str):
    prefixes=await prefix_cache[guild_id]
    assert isinstance(prefixes,list)
    if new_prefix in prefixes:
        raise ValueError("Prefix already exists!")
    async with pool.acquire() as conn:
        assert isinstance(conn,Connection)
        await conn.execute(f"UPDATE GuildData SET prefixes=$1 WHERE GuildID=$2",prefixes+[new_prefix],guild_id)
        prefix_cache.pop(guild_id)
async def remove_prefix(guild_id:int,prefix:str):
    async with pool.acquire() as conn:
        assert isinstance(conn,Connection)
        old_prefixes=await prefix_cache[guild_id]
        assert isinstance(old_prefixes,list)
        if prefix not in old_prefixes:
            raise LookupError("That prefix does not exist in the prefixes for this server!")
        old_prefixes.remove(prefix)
        prefix_cache.pop(guild_id)
        await conn.execute(f"UPDATE GuildData SET prefixes=$1 WHERE GuildID=$2",old_prefixes,guild_id)
async def insert_new_alias(guild_id:int,alias_name:str,alias_sprite:str):
    if alias_name in (await alias_cache[guild_id])[0]:
        raise ValueError("An alias with that name already exists!")
    async with pool.acquire() as conn:
        s=await alias_cache[guild_id]
        assert isinstance(conn,Connection) and isinstance(s,tuple)
        aliastext,aliassprites=s
        aliastext:List[str]
        aliassprites:List[str]
        await conn.execute(f"UPDATE GuildData SET AliasText=$1,AliasSprites=$2 WHERE GuildID=$3",aliastext+[alias_name],aliassprites+[alias_sprite],guild_id)
        alias_cache.pop(guild_id)
async def remove_alias(guild_id:int,alias_name:str):
    if alias_name not in (await alias_cache[guild_id])[0]:
        raise LookupError("Could not find that alias name in the server's aliases!")
    async with pool.acquire() as conn:
        assert isinstance(conn,Connection) and isinstance(s:=await alias_cache[guild_id],tuple)
        aliastext,aliassprites=s
        aliassprites.pop(aliastext.index(alias_name))
        aliastext.remove(alias_name)
        await conn.execute(f"UPDATE GuildData SET AliasText=$1,AliasSprites=$2 WHERE GuildID=$3",aliastext,aliassprites,guild_id)
        alias_cache.pop(guild_id)