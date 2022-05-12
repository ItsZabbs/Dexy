import discord
from discord.ext import commands

def support_field(embed:discord.Embed)->discord.Embed:
    embed.add_field(name='\u200b',value='Join the [support server](https://discord.gg/FBFTYp7nnq)')
    return embed
class MyCustomHelpCommand(commands.HelpCommand):
    def get_destination(self)->commands.Context:
        return self.context
    async def send_bot_help(self, mapping):
        ctx=self.get_destination()
        embed=discord.Embed(colour=ctx.me.colour if ctx.me.colour!=discord.Colour.default() else discord.Color.blurple())
        embed.set_author(name=f'{ctx.me.name} Help Dialogue! Bot page',url="https://discordbotlist.com/bots/pokedex-bot")
        embed.set_footer(text=f'Use {ctx.clean_prefix} help <category> for more info on \
a category\n Or use {ctx.clean_prefix} help <command> for more info on a command')
        for cog,commands in mapping.items():
            if not cog:
                continue
            name=cog.qualified_name if cog else "No Category"
            filtered_list=await self.filter_commands(commands,sort=True)
            commandlist=["`"+command.name+"`: "+(command.help.split("\n"))[0] if command.help else f"`{command.name}`: No Help provided" for command in filtered_list]
            if commandlist:
                embed.add_field(name=name,value="\n".join(commandlist),inline=False)
        embed=support_field(embed)
        await ctx.send(embed=embed)

    async def send_cog_help(self, cog:commands.Cog):
        command = cog.get_commands()
        ctx:commands.Context=self.get_destination()
        embed=discord.Embed(title=cog.qualified_name,description=cog.description,colour=ctx.me.colour if ctx.me.colour!=discord.Colour.default() else discord.Color.blurple())        
        embed.set_author(name=f'{ctx.me.name} Help Dialogue!')
        embed.set_footer(text=f'Use {ctx.clean_prefix} help <category> for more info on a \
category\n Or use {ctx.clean_prefix} help <command> for more info on a command')
        filtered_list=await self.filter_commands(command,sort=True)
        if filtered_list:
            for e in filtered_list:
                helper=e.help.split('\n')[0] if e.help else "No Help provided"
                embed.add_field(name=e.name,value=f"`{helper}`",inline=False)
            embed=support_field(embed)
            await ctx.send(embed=embed)
        else:
            await ctx.send("You cannot use any commands from there!")

    async def send_group_help(self, group:commands.Group):
        commands = list(group.commands)
        ctx=self.get_destination()
        embed=discord.Embed(title=f"Information on {group.qualified_name}",description=group.description,colour=ctx.me.colour if ctx.me.colour!=discord.Color.default() else discord.Color.blurple())        
        embed.set_author(name=f'{ctx.me.name} Help Dialogue!')
        embed.set_footer(text=f'Use {ctx.clean_prefix} help <category> for more info on a \
category\n Or use {ctx.clean_prefix} help <command> for more info on a command')
        filtered_list=await self.filter_commands(commands)
        if filtered_list:
            for e in filtered_list:
                helper=e.help.split('\n')[0] if e.help else "No Help provided"
                embed.add_field(name=e.name,value=f"`{helper}`",inline=False)
            embed=support_field(embed)
            await ctx.send(embed=embed)
        else:
            await ctx.send("You cannot use any commands from that command group!")
  
    async def send_command_help(self, command:commands.Command):
        ctx=self.get_destination()
        signature=self.get_command_signature(command)
        embed=discord.Embed(title=f'Information on `{command.name}`',description=f"```\n{command.help}\n```",colour=ctx.me.colour if ctx.me.colour!=discord.Color.default() else discord.Colour.blurple())
        embed.set_author(name=f'{ctx.me.name} Help Dialogue!')
        embed.set_footer(text=f'Use {ctx.clean_prefix} help <category> for more info on a \
category\n Or use {ctx.clean_prefix} help <command> for more info on a command')
        if command.aliases:
            embed.add_field(name='Aliases',value=f'`{"|".join(command.aliases)}`',inline=False)
        embed.add_field(name='Usage',value=f'`{signature}`',inline=False)
        embed=support_field(embed)
        await ctx.send(embed=embed)


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._original_help_command = bot.help_command
        help_command = MyCustomHelpCommand()
        help_command.cog = self  # Instance of YourCog class
        bot.help_command = help_command
    
    def cog_unload(self):
        self.bot.help_command = self._original_help_command

async def setup(bot):
    await bot.add_cog(Help(bot))

