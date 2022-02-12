import discord
from discord.ext import commands
import dotenv
import os
from glob import glob
import traceback


from ..db import db

# Loading the environment variables
dotenv.load_dotenv()
token = os.getenv("BOT_TOKEN")
error_guild_id = os.getenv("GUILD_ID")
error_channel_id = os.getenv("CHANNEL_ID")
feedback_channel_id=os.getenv("FEEDBACK_ID")
guild_logs_id=os.getenv('GUILD_LOG_ID')

intents = discord.Intents.default()

# Allowing mentions in messages of the bot
mentions = discord.AllowedMentions(everyone=False, users=True, roles=False, replied_user=True)

# Cogs
COGS = [path.split("\\")[-1][:-3] for path in glob("./lib/cogs/*.py")]
# Owner IDS
OWNER_ID = 650664682046226432

# Prefix cache implementation
prefix_cache={}

async def get_prefix(user,message):
    if message.guild is None:
        prefix = "dexy"
        return commands.when_mentioned_or(prefix)(user, message)
    elif message.guild.id in prefix_cache:
        return commands.when_mentioned_or(*prefix_cache[message.guild.id])(user, message)
    else:
        prefix=db.field("SELECT Prefix FROM guilds WHERE GuildID = ?",message.guild.id)
    try:
        prefix=prefix.split(",")
    except:
        prefix=['dexy']
    if len(prefix_cache)>120:
        prefix_cache.pop(tuple(prefix_cache.keys())[0])
    prefix_cache[message.guild.id]=prefix
    return commands.when_mentioned_or(*prefix_cache[message.guild.id])(user, message)


async def update():
    for guild in bot.guilds:
        try:
            db.execute("INSERT INTO guilds (GuildID) VALUES (?)", guild.id)
        except:
            pass

class Bot(commands.Bot):
    def __init__(self):
        self.TOKEN = token
        self.ready = False
        self.owner_id = OWNER_ID
        self.reconnect = True
        self.prefix_cache=prefix_cache
        self.feedback_webhook=feedback_channel_id
        super().__init__(case_insensitive=True, allowed_mentions=mentions, intents=intents,
                         command_prefix=get_prefix,strip_after_prefix=True,
                         owner_id=OWNER_ID,max_messages=None)


    def setup(self):
        for ext in os.listdir("./lib/cogs"):
            if ext.endswith(".py") and not ext.startswith("_"):
                try:
                    self.load_extension(f"lib.cogs.{ext[:-3]}")
                    print(f" {ext[:-3]} cog loaded")
                except Exception:
                    desired_trace = traceback.format_exc()
                    print(desired_trace)
        print("setup complete")
        self.load_extension('jishaku')
        print("jishaku loaded")
        print("setup complete")

    def run(self, version):

        print("running setup...")
        self.setup()

        print("running bot...")

        super().run(self.TOKEN, reconnect=True)

    async def process_commands(self, message):
        ctx = await self.get_context(message, cls=commands.Context)

        if ctx.command is not None:
            if not self.ready:
                await ctx.send("I'm not ready to receive commands. Please wait a few seconds.")

            else:
                await self.invoke(ctx)

    async def on_connect(self):
        await update()
        self.error_channel:discord.TextChannel=await self.fetch_channel(error_channel_id)
        self.error_webhook=await self.error_channel.webhooks()
        self.error_webhook=self.error_webhook[0]
        self.guild_log:discord.TextChannel=await self.fetch_channel(guild_logs_id)
        self.guild_log=await self.guild_log.webhooks()
        self.guild_log=self.guild_log[0]
        print("updated")
        print("bot connected")
        
    async def on_disconnect(self):
        print("bot disconnected")

    async def on_command_error(self, ctx:commands.Context, err):
        embed=discord.Embed(title='An error occurred',colour=ctx.me.colour)
        embed.add_field(name='Error description',value=f"```\n{err}\n```",inline=False)
        embed.add_field(name='Still confused?',value='Join the [support server](https://discord.gg/FBFTYp7nnq) and ask about this there!')
        try:
            await ctx.send(embed=embed)#f"Something went wrong \n ```\n{err}\n```")
        except:
            await ctx.author.send(f"I cannot send embeds or messages in {ctx.channel.mention}!")
        try:
            embed=discord.Embed(title='Error',description=f'{err}')
            embed.add_field(name='Command used -',value=f'{ctx.message.content}',inline=False)
            await self.error_webhook.send(embed=embed)
        except:
            raise err
    async def on_guild_join(self, guild:discord.Guild):
        try:
            db.execute("INSERT INTO guilds (GuildID) VALUES (?)", guild.id)
        except:
            pass
        embed=discord.Embed(title='Guild added',description=f'ID : {guild.id}\n NAME : {guild.name}\n OWNERID : {guild.owner_id}')#\n OWNER_NAME : {guild.owner.name}#{guild.owner.discriminator}')
        await self.guild_log.send(embed=embed)
    
    async def on_guild_remove(self, guild:discord.Guild):
        embed=discord.Embed(title='Guild left',description=f'ID : {guild.id}\n NAME : {guild.name}\n OWNERID : {guild.owner_id}')# OWNER_NAME : {guild.owner.name}#{guild.owner.discriminator}')
        await self.guild_log.send(embed=embed)
    
    
        
    # async def on_guild_(self, guild):
    #     db.execute("DELETE FROM guilds WHERE GuildID = ?", guild.id)
    async def on_message(self, message:discord.Message):
        if message.author.bot:return
        return await super().on_message(message)
    async def on_ready(self):
        await update()
        self.ready = True
        print("bot ready")


bot = Bot()
