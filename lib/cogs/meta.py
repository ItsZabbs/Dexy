import copy
from datetime import datetime, timedelta
from platform import python_version
from time import time
from typing import Union, Optional

import discord
from discord import Activity, ActivityType
from discord.ext import tasks
from discord.ext.commands import Context,CommandInvokeError,Cog,command,CheckFailure
from psutil import Process, virtual_memory

from ..db import db
from lib.bot import Bot

class Meta(Cog):
    '''Bot owner commands'''

    def __init__(self, bot:Bot):
        self.bot = bot
        self._message = "watching for dexy help | Report any errors to Zabbs#6530!"
    async def cog_check(self, ctx):
        assert ctx.command is not None
        if ctx.command.name=="stats":
            return True
        return ctx.author.id==650664682046226432
    @command(name='leaveguild')
    async def leaveguild(self,ctx,GuildID:Optional[discord.Guild]):
        if GuildID is None:GuildID=self.bot.get_guild(ctx.guild.id)
        assert GuildID is not None
        await GuildID.leave()
        assert self.bot.owner_id is not None and (owner:=self.bot.get_user(self.bot.owner_id)) is not None
        await owner.send(f"The bot has successfully left {GuildID.name}")
    @property
    def message(self):
        return self._message.format(users=len(self.bot.users), guilds=len(self.bot.guilds))

    @message.setter
    def message(self, value):
        if value.split(" ")[0] not in ("playing", "watching", "listening", "streaming"):
            raise ValueError("Invalid activity type.")

        self._message = value

    async def set(self):
        _type, _name = self.message.split(" ", maxsplit=1)

        await self.bot.change_presence(activity=Activity(
            name=_name, type=getattr(ActivityType, _type, ActivityType.playing)
        ))

    @command(name="setactivity")
    async def set_activity_message(self, ctx, *, text: str):
        '''Sets the status of the bot
        Can be either Playing,Watching,Listening or Streaming
        '''
        self.message = text
        await self.set()

    # @commands.command(name='load', hidden=True)
    # async def cogload(self, ctx, *, cog: str):
    #     """Command which Loads a Module.
    #     Remember to use dot path. e.g: cogs.owner"""

    #     try:
    #         self.bot.load_extension(cog)
    #     except Exception as e:
    #         await ctx.send(f'**ERROR:** {type(e).__name__} - {e}')
    #     else:
    #         await ctx.send('**SUCCESS**')

    # @commands.command(name='unload', hidden=True)
    # async def cogunload(self, ctx, *, cog: str):
    #     """Command which Unloads a Module.
    #     Remember to use dot path. e.g: cogs.owner"""

    #     try:
    #         self.bot.unload_extension(cog)
    #     except Exception as e:
    #         await ctx.send(f'**ERROR:** {type(e).__name__} - {e}')
    #     else:
    #         await ctx.send('**SUCCESS**')

    # @commands.command(
    #     name='reload'
    # )
    # async def reload(self, ctx, cog:Optional[commands.Cog]=None):
    #     '''"Reload all/one of the bots cogs!"'''
    #     if not cog:
    #         # No cog, means we reload all cogs
    #         async with ctx.typing():
    #             embed = discord.Embed(
    #                 title="Reloading all cogs!",
    #                 color=0x808080,
    #                 timestamp=ctx.message.created_at
    #             )
    #             for ext in os.listdir("./lib/cogs/"):
    #                 if ext.endswith(".py") and not ext.startswith("_"):
    #                     try:
    #                         self.bot.unload_extension(f"lib.cogs.{ext[:-3]}")
    #                         self.bot.load_extension(f"lib.cogs.{ext[:-3]}")
    #                         embed.add_field(
    #                             name=f"Reloaded: {ext}",
    #                             value='\uFEFF',
    #                             inline=False
    #                         )
    #                     except Exception as e:
    #                         embed.add_field(
    #                             name=f"Failed to reload: {ext}",
    #                             value=e,
    #                             inline=False
    #                         )
    #                     await asyncio.sleep(0.5)
    #             await ctx.send(embed=embed)
    #     else:
    #         async with ctx.typing():
    #             embed = discord.Embed(
    #                 title="Reloading all cogs!",
    #                 color=0x808080,
    #                 timestamp=ctx.message.created_at
    #             )
    #             ext = f"{cog.lower()}.py"
    #             if not os.path.exists(f"./lib/cogs/{ext}"):
    #                 # if the file does not exist
    #                 embed.add_field(
    #                     name=f"Failed to reload: {ext}",
    #                     value="This cog does not exist.",
    #                     inline=False
    #                 )

    #             elif ext.endswith(".py") and not ext.startswith("_"):
    #                 try:
    #                     self.bot.unload_extension(f"cogs.{ext[:-3]}")
    #                     self.bot.load_extension(f"cogs.{ext[:-3]}")
    #                     embed.add_field(
    #                         name=f"Reloaded: {ext}",
    #                         value='\uFEFF',
    #                         inline=False
    #                     )
    #                 except Exception:
    #                     desired_trace = traceback.format_exc()
    #                     embed.add_field(
    #                         name=f"Failed to reload: {ext}",
    #                         value=desired_trace,
    #                         inline=False
    #                     )
    #             await ctx.send(embed=embed)

    @command(name="stats")
    async def show_bot_stats(self, ctx):
        '''Shows the bot's stats'''
        embed = discord.Embed(title="Bot stats",
                              colour=ctx.author.colour,
                              timestamp=datetime.utcnow())
        assert self.bot.user is not None and self.bot.user.avatar is not None
        embed.set_thumbnail(url=self.bot.user.avatar.url)

        proc = Process()
        with proc.oneshot():
            uptime = timedelta(seconds=time() - proc.create_time())
            cpu_time = timedelta(seconds=(cpu := proc.cpu_times()).system + cpu.user)
            mem_total = virtual_memory().total / (1024 ** 2)
            mem_of_total = proc.memory_percent()
            mem_usage = mem_total * (mem_of_total / 100)

        fields = [
            ("Python version", python_version(), True),
            ("discord.py version", discord.__version__, True),
            ("Uptime", uptime, True),
            ("CPU time", cpu_time, True),
            ("Memory usage", f"{mem_usage:,.3f} / {mem_total:,.0f} MiB ({mem_of_total:.0f}%)", True),
        ]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        embed.set_footer(text="Wanted to see a Pokemon's stats? Try using the litedex command!")
        await ctx.send(embed=embed)
    
    @show_bot_stats.error
    async def stats_error(self,ctx,error):
        if isinstance(error,CheckFailure):
            await ctx.send("This command is reserved for the bot developer. You should try using the `ldex` command instead!")
    @command(name="shutdown")
    async def shutdown(self, ctx:Context):
        '''Shuts down the bot'''
        await ctx.send("Shutting down...")
        command=self.bot.get_command("jsk shutdown")
        if command is None:
            return await ctx.send("Jishaku is not loaded. Could not shutdown.")
        await ctx.invoke(command)#type:ignore

    @command(name='sudo')
    async def sudo(self, ctx: Context, user: Union[discord.Member, discord.User], *, command: str):
        """Run a command as another user."""
        msg = copy.copy(ctx.message)
        msg.author = user
        assert ctx.prefix is not None
        msg.content = ctx.prefix + command
        new_ctx = await self.bot.get_context(msg)
        try:
            await self.bot.invoke(new_ctx)
        except CommandInvokeError as e:
            raise e.original

    @Cog.listener()
    async def on_ready(self):
        print(f"{Meta.__qualname__} up")
async def setup(bot):
    await bot.add_cog(Meta(bot))
