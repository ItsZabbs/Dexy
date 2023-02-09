from discord.app_commands import command,guilds,Choice
from lib.bot import rpokemon_guild_id,secret_role_id,Bot
from lib.cogs.pokemon import move_names
from discord import Interaction,Role
from typing import Optional

role:Optional[Role]=None

@command(name='use',description='Use a move')
@guilds(rpokemon_guild_id)
async def use(interaction:Interaction,move:str):
    if move.lower().replace(" ","").strip()=="secretpower":
        await interaction.user.add_roles(roles=[role],reason='Used secret power')
        await interaction.response.send_message("You used Secret Power! You discovered #secret_base!")
    else:
        await interaction.response.send_message("There was no effect...")
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
    role=bot.get_guild(rpokemon_guild_id).get_role(secret_role_id)