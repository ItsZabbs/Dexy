import datetime
from asyncpg import UniqueViolationError
import traceback
from typing import Union
from psutil import Process,virtual_memory
from os import getpid

import discord
from discord.ext import commands, tasks
from lib.bot import Bot
from lib.db import db
from discord.ui import View


class ErrorModal(discord.ui.Modal, title="Error information"):
    error_info = discord.ui.TextInput(
        label="Any details that the developer should know?",
        max_length=1024,
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message("Thanks for your report!",ephemeral=True)


class ErrorView(View):
    def __init__(
        self,
        *,
        timeout: int = 180,
        message_link: str,
        feedback_webhook: discord.Webhook,
    ):
        super().__init__(timeout=timeout)
        self.webhook_message = message_link
        self.feedback_webhook = feedback_webhook

    @discord.ui.button(
        label="Report this error to the developer?",
        style=discord.ButtonStyle.green,
    ) #type:ignore
    async def submit_error(
        self, interaction: discord.Interaction, button: discord.Button
    ):
        modal = ErrorModal(timeout=5 * 60)
        await interaction.response.send_modal(modal)
        value = await modal.wait()
        if value:
            return await interaction.followup.send("Timed out.", ephemeral=True)
        await self.feedback_webhook.send(
            f"New error report submitted.\nUser info: {modal.error_info.value if modal.error_info.value else 'User did not provide any information.'}\nError Message: [Message Link]({self.webhook_message})"
        )
        self.stop()


class Events(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.guild_log = {"Added": 0, "Left": 0}
        self.mem_log = {}
        self.max_mem=virtual_memory().total
        self.process=Process()
    async def cog_load(self) -> None:
        self.post_guild_eod.start()
        return await super().cog_load()

    async def cog_unload(self) -> None:
        self.post_guild_eod.cancel()
        await self.bot.guild_webhook.send(
            f"Guilds added today: {self.guild_log['Added']}\nGuilds removed today: {self.guild_log['Left']}"
        )
        return await super().cog_unload()

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        try:
            async with self.bot.pool.acquire() as conn:
                await conn.execute("INSERT INTO GuildData (GuildID) VALUES ($1)", guild.id)
        except UniqueViolationError:
            title="Guild added which existed in DB before"
        else:
            title="Guild added"
        assert guild.owner_id is not None
        embed = discord.Embed(
            title=title,
            description=f"ID : {guild.id}\n NAME : {guild.name}\n OWNERID : {guild.owner_id}\n OWNER USERNAME: {await self.bot.fetch_user(guild.owner_id)}\n MEMBER COUNT: {guild.member_count}",
            colour=discord.Color.green(),
        )  # \n OWNER_NAME : {guild.owner.name}#{guild.owner.discriminator}')
        await self.bot.guild_webhook.send(embed=embed)
        self.guild_log["Added"] += 1

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        assert guild.owner_id is not None
        embed = discord.Embed(
            title="Guild left",
            description=f"ID : {guild.id}\n NAME : {guild.name}\n OWNERID : {guild.owner_id}\n OWNER USERNAME : {await self.bot.fetch_user(guild.owner_id)}\n MEMBER COUNT: {guild.member_count}",
            colour=discord.Color.red(),
        )  # OWNER_NAME : {guild.owner.name}#{guild.owner.discriminator}')
        await self.bot.guild_webhook.send(embed=embed)
        self.guild_log["Left"] += 1

    @commands.Cog.listener()
    async def on_command_error(
        self, ctx: Union[commands.Context, discord.Interaction], err: BaseException
    ):
        try:
            embed = discord.Embed(
                title="Error", description=err, colour=discord.Color.red()
            )
            
            if ctx.interaction is None:
                embed.add_field(
                    name="Command used -", value=ctx.message.content, inline=False
                )
                embed.add_field(
                    name="Command user - ",
                    value=f"{ctx.author} {ctx.author.id}",
                    inline=False,
                )
                message = await self.bot.error_webhook.send(embed=embed, wait=True)
            else:
                embed.add_field(
                    name="Command used -\n",
                    value=ctx.interaction.data["name"]
                    + " "
                    + " ".join(
                        [
                            v["name"] + " = " + str(v["value"])
                            for v in ctx.interaction.data.get("options", [])
                        ]
                    ),
                    inline=False,
                )
                embed.add_field(
                    name="Command user - ",
                    value=f"{ctx.interaction.user} {ctx.interaction.user.id}",
                    inline=False,
                )
                message = await self.bot.error_webhook.send(embed=embed, wait=True)
        except:
            traceback.print_exc(err)
        embed = discord.Embed(
            title="An error occurred - ",
            description=err,
            colour=ctx.me.colour if ctx.me.colour.value else discord.Colour.blurple(),
        )
        value = f'You can check the [wiki](https://ItsZabbs.github.io/Dexy{"#"+x if (x:=ctx.command.extras.get("url","").lower()) else ""})\n{"Or you can [join the support server](https://discord.gg/FBFTYp7nnq)" if ctx.guild and ctx.guild.id!=self.bot.rpokemon_guild_id else ""}'
        embed.add_field(name="Still confused?", value=value)
        view = ErrorView(
            message_link=message.jump_url, feedback_webhook=self.bot.feedback_webhook
        )
        if ctx.guild is None:
            await ctx.send(embed=embed, view=view)
        try:
            perms = ctx.channel.permissions_for(ctx.guild.me)
            if perms.send_messages and perms.embed_links:
                await ctx.send(embed=embed, view=view)
            elif perms.send_messages:
                return await ctx.send(
                    "Please ensure that I have the SEND MESSAGES and EMBED LINKS permissions here"
                )
            else:
                return await ctx.author.send(
                    f"Please ensure that I have the **SEND MESSAGES AND EMBED LINKS** permissions in {ctx.channel.mention}"
                )
        except discord.HTTPException as err:
            raise err
        except AttributeError:
            pass

    @tasks.loop(
        time=datetime.time(
            hour=0,
            minute=0,
            second=0,
            tzinfo=datetime.timezone(datetime.timedelta(hours=5.5)),
        )
    )
    async def post_guild_eod(self):
        if self.guild_log['Added']==self.guild_log['Left'] and self.guild_log['Left']==0:return
        await self.bot.guild_webhook.send(
            f"Guilds added today: {self.guild_log['Added']}\nGuilds removed today: {self.guild_log['Left']}"
        )
        self.guild_log.update({"Added": 0, "Left": 0})
    @commands.Cog.listener('on_command_completion')
    async def on_ext_command_completion(self,ctx:commands.Context):
        assert ctx.command is not None
        await self.command_stats(ctx.command.name,ctx.message.id)

    @commands.Cog.listener('on_app_command_completion')
    async def on_app_command_completion(self,interaction:discord.Interaction,command:discord.app_commands.Command):
        await self.command_stats(command.name,interaction.id)

    async def command_stats(self,cmdname:str,cmdid:int):
        async with self.bot.pool.acquire() as conn:
            import asyncpg
            conn:asyncpg.Connection
            record:list[asyncpg.Record]=await conn.fetch("SELECT usage,memusage from cmdstats where cmdname=$1",cmdname)
            if not record:return
            await conn.execute("update cmdstats set usage=usage+1 where cmdname=$1",cmdname)

async def setup(bot: Bot):
    await bot.add_cog(Events(bot))
    