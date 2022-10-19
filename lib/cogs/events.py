from typing import Union

import discord
from discord.ext import commands
from lib.bot import Bot


class Events(commands.Cog):
    def __init__(self,bot:Bot):
        self.bot=bot
    @commands.Cog.listener()
    async def on_command_error(self, ctx:Union[commands.Context,discord.Interaction], err:BaseException):
        embed=discord.Embed(title='An error occurred - ',description=err,colour=ctx.me.colour if ctx.me.colour.value else discord.Colour.blurple())
        value='Ask about this in the [support server](https://discord.gg/FBFTYp7nnq)'
        value+=f' \n or you can check the [wiki](https://ItsZabbs.github.io/Pokedex-Bot{"#"+x if (x:=ctx.command.extras.get("url","").lower()) else ""})'
        embed.add_field(name='Still confused?',value=value)
        if ctx.guild is None:
            await ctx.send(embed=embed)
        try:
            perms=ctx.channel.permissions_for(ctx.guild.me)
            if perms.send_messages and perms.embed_links:
                await ctx.send(embed=embed)
            elif perms.send_messages:
                await ctx.send("Please ensure that I have the SEND MESSAGES and EMBED LINKS permissions here")
            else:
                await ctx.author.send(f"Please ensure that I have the **SEND MESSAGES AND EMBED LINKS** permissions in {ctx.channel.mention}")
        except discord.HTTPException as err:
            raise err
        try:
            embed=discord.Embed(title='Error',description=err,colour=discord.Color.red())
            if ctx.interaction is None:
                embed.add_field(name='Command used -',value=ctx.message.content,inline=False)
                embed.add_field(name='Command user - ',value=ctx.author.id,inline=False)
                await self.bot.error_webhook.send(embed=embed)
            else:
                embed.add_field(name='Command used -\n',value=ctx.interaction.data["name"]+" "+" ".join([v["name"]+" = "+v["value"] for v in ctx.interaction.data.get("options",[])]),inline=False)
                embed.add_field(name='Command user - ',value=ctx.interaction.user.id,inline=False)
                await self.bot.error_webhook.send(embed=embed)
        except:
            raise err
            
async def setup(bot:Bot):
    await bot.add_cog(Events(bot))