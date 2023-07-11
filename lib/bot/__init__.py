import asyncpg
import discord
from discord.ext import commands
import dotenv
import os
import traceback
import logging
from asyncpg import Connection
from asyncpg.exceptions import UniqueViolationError

from ..db import db

# Loading the environment variables
dotenv.load_dotenv()
token = os.getenv("BOT_TOKEN")
test_token=os.getenv("TEST_BOT_TOKEN")
error_webhook = os.getenv("ERROR_WEBHOOK")
feedback_webhook=os.getenv("FEEDBACK_WEBHOOK")
guild_webhook=os.getenv('GUILD_WEBHOOK')
command_webhook=os.getenv('COMMAND_WEBHOOK')
rpokemon_guild_id=os.getenv('RPOKEMON_GUILD_ID')
secret_role_id=os.getenv('SECRET_ROLE_ID')
assert None not in (token,error_webhook,feedback_webhook,guild_webhook,command_webhook,rpokemon_guild_id,secret_role_id)

intents = discord.Intents.none()
intents.messages=True
intents.guilds=True
intents.message_content=True

# Allowing mentions in messages of the bot
mentions = discord.AllowedMentions(everyone=False, users=True, roles=False, replied_user=True)

# Owner IDS
assert (OWNER_ID:=os.getenv("OWNER_ID")) is not None and OWNER_ID.isdigit()
OWNER_ID=int(OWNER_ID)
#Logging
discord.utils.setup_logging(level=logging.INFO)

# Prefix cache implementation
prefix_cache={}

async def get_prefix(user,message):
    #return commands.when_mentioned_or("dd")(user, message)
    if message.guild is None:
        prefix = "dexy"
        return commands.when_mentioned_or(prefix)(user, message)
    assert isinstance(s:=await db.prefix_cache[message.guild.id],list)
    return commands.when_mentioned_or(*s)(user,message)

            
class Bot(commands.AutoShardedBot):
    def __init__(self):
        self.TOKEN = token
        self.ready = False
        self.reconnect = True
        self.prefix_cache=db.prefix_cache
        self.alias_cache=db.alias_cache
        assert isinstance(rpokemon_guild_id,str)
        self.rpokemon_guild_id=int(rpokemon_guild_id)
        super().__init__(case_insensitive=True, allowed_mentions=mentions, intents=intents,
                         command_prefix=get_prefix,strip_after_prefix=True,
                         owner_id=OWNER_ID,max_messages=None)


    async def setup_hook(self):
        assert isinstance(error_webhook,str) and isinstance(feedback_webhook,str) and isinstance(guild_webhook,str) and isinstance(command_webhook,str)
        self.error_webhook=await self.fetch_webhook(int(error_webhook))
        self.feedback_webhook=await self.fetch_webhook(int(feedback_webhook))
        self.guild_webhook=await self.fetch_webhook(int(guild_webhook))
        self.command_webhook=await self.fetch_webhook(int(command_webhook))
        for ext in reversed(os.listdir("./lib/cogs")): #temp fix to let moveset load after pokemon is loaded
            if ext.endswith(".py") and not ext.startswith("_"):
                try:
                    await self.load_extension(f"lib.cogs.{ext[:-3]}")
                    print(f" {ext[:-3]} cog loaded")
                except Exception:
                    desired_trace = traceback.format_exc()
                    print(desired_trace)
                    
        await self.load_extension('jishaku')
        self.pool=await db.setup_database()
        
    async def start(self,test:bool=False) -> None:
        bot_token=token if not test else test_token
        assert isinstance(bot_token,str)
        await super().start(bot_token, reconnect=True)

    async def process_commands(self, message):
        ctx = await self.get_context(message, cls=commands.Context)

        if ctx.command is not None:
            if not self.ready:
                await ctx.send("I'm not ready to receive commands. Please wait a few seconds.")

            else:
                await self.invoke(ctx)

    async def on_connect(self):
        print("Connected")

    async def on_message(self, message:discord.Message):
        if message.author.bot:return
        if message.author == self.user:return
        return await super().on_message(message)
    async def on_ready(self):
        self.ready = True


bot = Bot()
