import aiohttp
import discord
from discord.ext import commands,tasks
import dotenv
import os
import traceback
import asyncio

import logging
import datetime

from ..db import db

# Loading the environment variables
dotenv.load_dotenv()
token = os.getenv("BOT_TOKEN")
test_token=os.getenv("TEST_BOT_TOKEN")
error_webhook = os.getenv("ERROR_WEBHOOK")
feedback_webhook=os.getenv("FEEDBACK_WEBHOOK")
guild_webhook=os.getenv('GUILD_WEBHOOK')
logs_webhook=os.getenv('COMMAND_WEBHOOK')
rpokemon_guild_id=os.getenv('RPOKEMON_GUILD_ID')
secret_role_id=os.getenv('SECRET_ROLE_ID')
assert None not in (token,error_webhook,feedback_webhook,guild_webhook,logs_webhook,rpokemon_guild_id,secret_role_id)

intents = discord.Intents.none()
intents.messages=True
intents.guilds=True
intents.message_content=True

# Allowing mentions in messages of the bot
mentions = discord.AllowedMentions(everyone=False, users=True, roles=False, replied_user=True)

# Owner IDS
assert (OWNER_ID:=os.getenv("OWNER_ID")) is not None and OWNER_ID.isdigit()
OWNER_ID=int(OWNER_ID)

# Logging set up
class EmbedWebhookLogger:
    _to_log:list[discord.Embed]

    def __init__(self, webhook_url:str):
        self.webhook_url=webhook_url
        self._to_log=[]
        self.loop=asyncio.get_event_loop()
        
        self._session = aiohttp.ClientSession()
        self._webhook = discord.Webhook.from_url(webhook_url, session=self._session)

    def log(self, embed: discord.Embed) -> None:
        self._to_log.append(embed)
    
    @tasks.loop(seconds=5)
    async def _loop(self):
        while self._to_log:
            embeds=[]
            while len(embeds)<10 and self._to_log:
                embeds.append(self._to_log.pop(0))
                next=self._to_log[0]
                if sum(map(len,embeds))+len(next)>6000: #max embed length is 6000
                    break
                embeds.append(self._to_log.pop(0))
            await self._webhook.send(embeds=embeds)

class WebhookHandler(logging.Handler):
    _colours = {
        logging.DEBUG: discord.Colour.light_grey(),
        logging.INFO: discord.Colour.gold(),
        logging.WARNING: discord.Colour.orange(),
        logging.ERROR: discord.Colour.red(),
        logging.CRITICAL: discord.Colour.dark_red(),
    }

    def __init__(self, webhook_url: str, level: int = logging.NOTSET) -> None:
        super().__init__(level)
        self._webhook_logger = EmbedWebhookLogger(webhook_url)

    def emit(self, record: logging.LogRecord) -> None:
        self.format(record)

        message = f'{record.message}\n{record.exc_text or ""}'
        message = message[:1987] + "..." if len(message) > 1987 else message

        self._webhook_logger.log(
            discord.Embed(
                colour=self._colours.get(record.levelno),
                title=record.name,
                description=f"```py\n{message}```",
                timestamp=datetime.datetime.fromtimestamp(record.created),
            ).add_field(name="\N{ZERO WIDTH SPACE}", value=f"{record.filename}:{record.lineno}")
        )

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
        assert isinstance(error_webhook,str) and isinstance(feedback_webhook,str) and isinstance(guild_webhook,str) and isinstance(logs_webhook,str)
        self.error_webhook=await self.fetch_webhook(int(error_webhook))
        self.feedback_webhook=await self.fetch_webhook(int(feedback_webhook))
        self.guild_webhook=await self.fetch_webhook(int(guild_webhook))
        for ext in sorted(os.listdir("./lib/cogs"),reverse=True): #temp fix to let moveset load after pokemon is loaded
            if ext.endswith(".py") and not ext.startswith("_"):
                try:
                    await self.load_extension(f"lib.cogs.{ext[:-3]}")
                    print(f" {ext[:-3]} cog loaded")
                except Exception:
                    desired_trace = traceback.format_exc()
                    print(desired_trace)
                    
        await self.load_extension('jishaku')
        webhook_logging=WebhookHandler(logs_webhook, level=logging.INFO)
        discord.utils.setup_logging(handler=webhook_logging)
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
