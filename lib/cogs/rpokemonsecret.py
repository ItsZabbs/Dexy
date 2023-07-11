from discord.app_commands import command,guilds,Choice
from lib.bot import rpokemon_guild_id,secret_role_id,Bot
from lib.cogs.pokemon import move_names
from discord import Interaction,Role,Object,Member,Role,Guild
from typing import Optional

role:Optional[Role]=None
assert rpokemon_guild_id is not None and secret_role_id is not None

@command(name='use',description='Use a move')
@guilds(Object(rpokemon_guild_id))
async def use(interaction:Interaction,move:str):
    assert isinstance(interaction.user,Member) and isinstance(interaction.guild,Guild)
    assert role is not None
    if move.lower().replace(" ","").strip().replace("-","")=="secretpower":
        await interaction.user.add_roles(role,reason='Used secret power')
        await interaction.response.send_message(f"You used Secret Power! You discovered {getattr(interaction.guild.get_channel(1071525828933992488),'mention','#secret_base')}!",ephemeral=True)
    else:
        await interaction.response.send_message("There was no effect...",ephemeral=True)
@use.autocomplete(name='move')
async def autocomplete(interaction:Interaction,current:str):
    return [
            Choice(name=move.replace("-", " ").capitalize(), value=move)
            for move in move_names
            if current.lower() in move.replace("-"," ").lower()
        ][:25]
async def setup(bot:Bot):
    bot.tree.add_command(use)
    global role
    role=(await bot.fetch_guild(int(rpokemon_guild_id))).get_role(int(secret_role_id))
    assert isinstance(role,Role)