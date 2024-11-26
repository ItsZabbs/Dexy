from typing import Dict, List, Mapping, Optional
import discord
from discord.ext import menus,commands
from discord import ui
from discord.ext.commands import Command,Cog
USER_HELP_MENU_LIST=[
                    discord.SelectOption(label='Pokemon',value='0',description='Pokemon information related',emoji="<:Pokeball:743294950355107861>"),
                    discord.SelectOption(label='Misc',value='1',description='Miscellaneous.',emoji="❓"),
                    discord.SelectOption(label='Meta',value='2',description='Bot statistics related.',emoji='ℹ️'),
                    discord.SelectOption(label='Help',value='3',description='Help command')
                    ]

def support_field(embed:discord.Embed,name="")->discord.Embed:
    embed.add_field(name='\u200b',value=f'Check the [wiki](https://itszabbs.github.io/Dexy#{name}) for detailed documentation')
    return embed
class HelpPageSource(menus.ListPageSource):
    def __init__(self, data, helpcommand):
        super().__init__(data, per_page=1)
        self.helpcommand = helpcommand
    async def get_page(self, page_number):
        return self.entries[page_number]

    def format_command_help(self,key,value):
        return f"**{key}**",value
    async def format_page(self, menu, entries:dict[str,dict[str,str]]):
        page = menu.current_page
        max_page = self.get_max_pages()
        page_content = "**"+tuple(entries.keys())[0]+":**"
        embed = discord.Embed(
            title=f"Pokedex Bot Help Dialogue ({page + 1}/{max_page})", 
            description=f"Currently viewing help for {page_content}",
            color=discord.Colour.blurple() if menu.ctx.author.colour.value else menu.ctx.author.colour
        )
        for command,help_string in tuple(entries.values())[0].items():
            embed.add_field(name="**"+command+"**",value=help_string,inline=False)
        author = menu.ctx.author
        embed.set_footer(text=f"Requested by {author}", icon_url=author.avatar.url)
        return embed
    

class SelectNew(discord.ui.Select):
    def __init__(self,options:list):
        super().__init__(placeholder="Select an option",max_values=1,min_values=1,options=options,custom_id="new_help")
    async def callback(self, interaction: discord.Interaction):
        return self.values[0]

class MyMenuPages(ui.View, menus.MenuPages):
    def __init__(self, source, *, delete_message_after=False):
        super().__init__(timeout=60)
        self._source = source
        self.current_page = 0
        self.ctx = None
        self.message:Optional[discord.Message] = None
        self.delete_message_after = delete_message_after
    async def on_timeout(self) -> None:
        self.select_menu.disabled=True
        for item in self.children:
            item.disabled=True#type:ignore
        assert self.message is not None
        await self.message.edit(view=self)
    async def send_initial_message(self, ctx, channel):
        return await super().send_initial_message(ctx, channel)
    async def start(self, ctx, *, channel=None, wait=False):
        await self._source._prepare_once()
        self.ctx = ctx
        self.message = await self.send_initial_message(ctx, ctx.channel)
    async def _get_kwargs_from_page(self, page):
        value = await super()._get_kwargs_from_page(page)
        assert value is not None
        if 'view' not in value:
            value.update({'view': self})
        return value

    async def interaction_check(self, interaction):
        """Only allow the author to be able to use the interaction"""
        assert self.ctx is not None
        return interaction.user == self.ctx.author
    @ui.select(placeholder='Select a category',options=USER_HELP_MENU_LIST)
    async def select_menu(self,interaction:discord.Interaction,select_value:ui.Select):
        await self.show_checked_page(int(select_value.values[0]))
        await interaction.response.defer()

    @ui.button(emoji='⏮️', style=discord.ButtonStyle.red)
    async def first_page(self, interaction, button):
        await self.show_page(0)
        await interaction.response.defer()

    @ui.button(emoji='⏪', style=discord.ButtonStyle.blurple)
    async def before_page(self, interaction, button):
        await self.show_checked_page(self.current_page - 1)
        await interaction.response.defer()

    @ui.button(emoji='🛑', style=discord.ButtonStyle.gray)
    async def stop_page(self, interaction, button):
        await interaction.response.defer()
        self.stop()
        if self.delete_message_after:
            assert self.message is not None
            await self.message.delete(delay=0)

    @ui.button(emoji='⏩', style=discord.ButtonStyle.blurple)
    async def next_page(self, interaction, button):
        await self.show_checked_page(self.current_page + 1)
        await interaction.response.defer()

    @ui.button(emoji='⏭️', style=discord.ButtonStyle.red)
    async def last_page(self, interaction, button):
        await self.show_page(self._source.get_max_pages() - 1)
        await interaction.response.defer()
    

class MyHelp(commands.MinimalHelpCommand):
    def get_command_brief(self, command):
        return command.short_doc or "Command is not documented."
    def clean_prefix(self,ctx:commands.Context):
        return ctx.clean_prefix if hasattr(ctx,"clean_prefix") else "dexy "
    def get_destination(self) -> commands.Context:
        return self.context
    async def send_bot_help(self, mapping:Mapping[Optional[Cog],List[Command]]):
        all_commands:Dict[int,Dict[str,Dict[str,str]]]=dict()
        for command in mapping[None]:
            if command.extras.get('helpcog',None) is not None:
                parentcog_commands=mapping.get(command.extras['helpcog'])
                if parentcog_commands is None:continue
                parentcog_commands.append(command)
                mapping[None].remove(command)
        #sorted_mapping=dict(sorted(mapping.items(),key=lambda item:item[0].qualified_name if item[0] else "No Category"),reverse=True)
        for cog,commands in mapping.items():
            i=None
            commandlist=dict()
            # if not cog:
            #     continue
            name=cog.qualified_name if cog else "No Category"
            filtered_list=await self.filter_commands(commands,sort=True)
            for command in filtered_list:
                commandlist[command.name]=(command.help.split("\n"))[0].replace("[prefix]",self.clean_prefix(self.context)) if command.help else "No Help provided"
            if commandlist:
                if name=="Pokemon":i=0
                elif name=="Misc":i=1
                elif name=="Meta":i=2
                elif name=="Help":i=3
                if i is None:
                    continue
                all_commands[i]={name:commandlist}      
        #all_commands=dict(sorted(all_commands.items(), key=lambda item:tuple(item[1].keys())[0]))
        formatter = HelpPageSource(all_commands, self)
        menu = MyMenuPages(formatter, delete_message_after=True)
        await menu.start(self.context)
    async def send_cog_help(self, cog:commands.Cog):
        command = cog.get_commands()
        command+=getattr(cog,'extracommands',[])
        ctx:commands.Context=self.get_destination()
        embed=discord.Embed(title=cog.qualified_name,description=cog.description,colour=ctx.me.colour if ctx.me.colour!=discord.Colour.default() else discord.Color.blurple())        
        embed.set_author(name=f'{ctx.me.name} Help Dialogue!')
        embed.set_footer(text=f'Use {self.clean_prefix(ctx)} help <category> for more info on a \
category\n Or use {self.clean_prefix(ctx)} help <command> for more info on a command')
        filtered_list=await self.filter_commands(command,sort=True)
        if filtered_list:
            for e in filtered_list:
                #helper=e.help.split('\n')[0] if e.help else "No Help provided"
                helper=e.help.split("\n")[0].replace("[prefix]",self.clean_prefix(ctx)) if e.help else "No Help provided"
                embed.add_field(name=e.name,value=helper,inline=False)
            url=getattr(cog,"url","")
            embed=support_field(embed,url)
            await ctx.send(embed=embed)
        else:
            await ctx.send("You cannot use any commands from there!")
    async def send_group_help(self, group:commands.Group):
        commands = list(group.commands)
        ctx=self.get_destination()
        embed=discord.Embed(title=f"Information on {group.qualified_name}",description=group.description,colour=ctx.me.colour if ctx.me.colour!=discord.Color.default() else discord.Color.blurple())        
        embed.set_author(name=f'{ctx.me.name} Help Dialogue!')
        embed.set_footer(text=f'Use {self.clean_prefix(ctx)} help <category> for more info on a \
category\n Or use {self.clean_prefix(ctx)} help <command> for more info on a command')
        filtered_list=await self.filter_commands(commands)
        if filtered_list:
            for e in filtered_list:
                #helper=e.help.split('\n')[0] if e.help else "No Help provided"
                helper=e.help.split("\n")[0].replace("[prefix]",self.clean_prefix(ctx)) if e.help else "No Help provided"
                embed.add_field(name=e.name,value=helper,inline=False)
            embed=support_field(embed,group.extras.get("url",""))
            await ctx.send(embed=embed)
        else:
            await ctx.send("You cannot use any commands from that command group!")
    async def send_command_help(self, command:commands.Command):
        ctx=self.get_destination()
        names=command.clean_params.values()
        signature=self.get_command_signature(command).replace(" [private=False]","")
        arg_desc=""
        for name,argument in command.clean_params.items():
            if name=='private':
                continue
            arg_desc=arg_desc+"\n"+"`"+name+"`: "+(argument.description or "No Help provided")
        embed=discord.Embed(title=f'Information on `{command.name}`',description=f"```\n{command.help}\n```",colour=ctx.me.colour if ctx.me.colour!=discord.Color.default() else discord.Colour.blurple())
        embed.set_author(name=f'{ctx.me.name} Help Dialogue!')
        embed.set_footer(text=f'Use {self.clean_prefix(ctx)} help <category> for more info on a \
category\n Or use {self.clean_prefix(ctx)} help <command> for more info on a command')
        if command.aliases:
            embed.add_field(name='Aliases',value=f'`{"|".join(command.aliases)}`',inline=False)
        embed.add_field(name='Usage',value=f'`{signature}`\n\n{arg_desc}',inline=False)
        embed=support_field(embed,command.extras.get("url",""))
        await ctx.send(embed=embed)
    

class Help(commands.Cog):
    url="help"
    def __init__(self, bot):
        self.bot = bot
        self._original_help_command = bot.help_command
        help_command = MyHelp()
        help_command.cog = self 
        bot.help_command = help_command
        
    def cog_unload(self):
        self.bot.help_command = self._original_help_command

async def setup(bot):
    await bot.add_cog(Help(bot))