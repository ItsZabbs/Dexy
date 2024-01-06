from lib.bot import Bot
from lib.cogs.pokemon import Pokemon
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import parameter
import discord
import difflib
from copy import copy,deepcopy
from typing import Dict, List

from .pokemon import Pokemon,moveid_dict, pokedex_dict, add_info_to_embed,serebii

from lib.cogs.utils import load_files_into_variable
from lib.cogs.utils.autocomplete import pokemon_autocomplete
from lib.cogs.utils.converters import PokemonConverter,get_close_matches
inverse_moveid_dict:Dict[str,int]={}
for k,v in moveid_dict.items():
    inverse_moveid_dict[v]=k
version_names = [
    "Red, Blue",
    "Yellow",
    "Gold, Silver",
    "Crystal",
    "Ruby, Sapphire",
    "Emerald",
    "Firered, Leafgreen",
    "Diamond, Pearl",
    "Platinum",
    "Heartgold, Soulsilver",
    "Black, White",
    "Colosseum",
    "Xd",
    "Black 2, White 2",
    "X, Y",
    "Omega Ruby, Alpha Sapphire",
    "Sun, Moon",
    "Ultra Sun, Ultra Moon",
    "Lets Go Pikachu, Lets Go Eevee",
    "Sword, Shield",
    "Brilliant Diamond, Shining Pearl",
    "Legends Arceus",
    "Scarlet, Violet"
]
learn_list = {
    "level-up": {"id": 1},
    "egg": {"id": 2},
    "tutor": {"id": 3},
    "tm": {"id": 4},
    "technical machine": {"id": 4},
    "stadium-surfing-pikachu": {"id": 5},
    "light-ball-egg": {"id": 6},
    "colosseum-purification": {"id": 7},
    "xd-shadow": {"id": 8},
    "xd-purification": {"id": 9},
    "form-change": {"id": 10},
    "zygarde-cube": {"id": 11},
}
learn_list_better = {1: 'Level Up', 2: 'Egg', 3: 'Tutor', 4: 'Technical Machine', 5: 'Stadium Surfing Pikachu',
                     6: 'Light Ball Egg', 7: 'Colosseum Purification', 8: 'Xd Shadow', 9: 'Xd Purification', 10: 'Form Change', 11: 'Zygarde Cube'}
version_dict = {
    "red-blue": "1",
    "yellow": "2",
    "gold-silver": "3",
    "crystal": "4",
    "ruby-sapphire": "5",
    "emerald": "6",
    "firered-leafgreen": "7",
    "diamond-pearl": "8",
    "platinum": "9",
    "heartgold-soulsilver": "10",
    "black-white": "11",
    "colosseum": "12",
    "xd": "13",
    "black 2-white 2": "14",
    "x-y": "15",
    "omega ruby-alpha sapphire": "16",
    "sun-moon": "17",
    "ultra sun-ultra moon": "18",
    "lets go pikachu-lets go eevee": "19",
    "sword-shield": "20",
    "brilliant diamond-shining pearl": "21",
    "legends arceus": "99",
    "scarlet-violet":"22"
}
initial_dict = {
    "rb": "1",
    "y": "2",
    "gs": "3",
    "c": "4",
    "rs": "5",
    "e": "6",
    "frlg": "7",
    "dp": "8",
    "pt": "9",
    "hgss": "10",
    "bw": "11",
    "co": "12",
    "xd": "13",
    "b2w2": "14",
    "xy": "15",
    "oras": "16",
    "sm": "17",
    "usum": "18",
    "lgp": "19",
    "lge": "19",
    "swsh": "20",
    "bdsp": "21",
    "pla": "99",
    "sv":"22"
}

movesets:Dict[str,Dict[str,Dict[str,List[Dict[str,int]]]]]=load_files_into_variable("lib/cogs/pokedexdata/movesets.json")
PokedexConverter=PokemonConverter(list(pokedex_dict.keys()),True)
def with_cog(cog: commands.Cog):
    def inner(command: commands.Command):
        command.extras = {'helpcog':cog}
        return command

    return inner
async def load_movesets_of_pokemon(pokemon_number,version_name,learn_type_id:str|None,ctx:commands.Context|discord.Interaction):
    pokemon_moves=movesets.get(str(pokemon_number),None)
    send_func=ctx.response.send_message if isinstance(ctx,discord.Interaction) else ctx.send
    if pokemon_moves is None:
        await send_func("Could not find the pokemon's movesets. Maybe the pokemon's moves aren't added yet.",ephemeral=True)
        return None
    pokemon_moves=pokemon_moves.get(str(version_name),None)
    if pokemon_moves is None:
        await send_func("That Pokemon doesn't exist in that game, or the developer is yet to add the movesets for that Pokemon for that game.",ephemeral=True)
        return None
    
    if learn_type_id is None:
        return pokemon_moves
    pokemon_moves=pokemon_moves.get(learn_type_id,None)
    if pokemon_moves is None:
        await send_func("That Pokemon doesn't learn any moves through that learn method.",ephemeral=True)
        return None
    return pokemon_moves

# @with_cog(Pokemon)
@commands.hybrid_command(name="moveset", extras={"url": "movesets"})
@app_commands.describe(
    pokemon="The Pokemon you want to get the moveset of",
    game_name="The game you want to get the moveset of",
    learn_type="The learning method of the moves",
    private="If only you want to see the moveset",
)
async def moveset(
    ctx: commands.Context,
    pokemon: PokedexConverter = parameter(description="The Pokemon you want to see the moveset of."), #type:ignore
    game_name: str = parameter(
        description="The name of the game. Eg. Omega Ruby or use initials like ORAS"
    ),
    learn_type: str = parameter(
        description="The learning method you want to see the moveset of.",
        default="level-up",
    ),
    private: bool = parameter(
        description="If only you want to see the moveset. Slash commands only.",
        default=False,
    ),
):
    """Sends the pokemon's moveset in the requested game. See [prefix]help moveset for more info"""
    pokemon_info=pokedex_dict[pokemon]
    colour = pokemon_info["color"]
    name = pokemon_info["name"]
    number = pokemon_info["num"]
    url=pokemon_info.get("url","")
    game_name = game_name.lower()
    version_name = initial_dict.get(game_name, None)
    if version_name is None:
        version_name = get_close_matches(game_name, version_dict.keys(),cutoff=0.3)
        if version_name is None:
            raise KeyError("I couldn't find the game you're looking for...")
        split_game_name = version_name.split("-")
        version_num = version_dict[version_name]
    else:
        split_game_name=list(version_dict.keys())[list(version_dict.values()).index(version_name)].split("-")
    learn_type_id = get_close_matches(learn_type, learn_list.keys(), cutoff=0.1)
    if learn_type_id is None:
        raise KeyError("I couldn't find the move learning method you're looking for...")
    movemethod = learn_type_id
    learn_type_id = str(learn_list[learn_type_id]["id"])
    pokemon_moves=await load_movesets_of_pokemon(number,version_name,learn_type_id,ctx)
    if pokemon_moves is None:
        return
    assert isinstance(pokemon_moves,list)
    if pokemon_moves[0].get("level", None) is None and version_name!="99": #Fix for movesets that are common amongst generations.Eg. Movesets for R,S are available in Emerald only.
        pokemon_moves=await load_movesets_of_pokemon(number,str(int(version_name)-1),learn_type_id,ctx)
    if pokemon_moves is None:
        return
    assert isinstance(pokemon_moves,list)
    bylevel = {}
    for d in sorted(pokemon_moves,key=lambda x:x.get('level',1)):
        level = d.get("level", "N/A")
        ls = bylevel.get(level, [])    
        ls.append([{k:v} for k,v in d.items() if k!="level"][0])
        bylevel.update({level: ls})
    colour = discord.Color.from_rgb(*colour)
    embed = discord.Embed(
        title=name.capitalize(),
        description=f'Move method - {" ".join([e.capitalize() for e in movemethod.split("-")])} \nGame - {", ".join(e.capitalize() if len(e.split())==0 else " ".join([i.capitalize() for i in e.split(" ")]) for e in split_game_name)}',
        colour=colour,
    )
    for k, v in bylevel.items():
        n = []
        for i in v:
            n.append(
                " ".join([e.capitalize() for e in moveid_dict[i["move_id"]].split("-")])
            )
            name = f"Level {k}" if k != 0 else "Level N/A"
        embed.add_field(name=name, value=", ".join(n), inline=False)
    embed.set_thumbnail(url=serebii+url)
    embed = await add_info_to_embed(ctx, embed)
    return await ctx.send(embed=embed, ephemeral=private)


@moveset.autocomplete("pokemon")
@pokemon_autocomplete
async def moveset_pokemon_auto(interaction, current):
    ...


@moveset.autocomplete("game_name")
async def moveset_gamename_auto(interaction, current):
    return [
        app_commands.Choice(name=e, value=e)
        for e in version_names
        if current.lower() in e.lower()
    ][:25]


@moveset.autocomplete("learn_type")
async def moveset_learntype_auto(interaction, current):
    return [
        app_commands.Choice(name=e.capitalize().replace("-", " "), value=e)
        for e in learn_list.keys()
        if current.lower() in e.lower()
    ][:25]
@app_commands.describe(pokemon="The pokemon whose learnset you want to check",move_name="The move you want to check for",game_name="The game whose moveset should be selected",private="If you want to invoke this command privately")
@app_commands.command(name="can_learn",description="Check if a pokemon learns a move")
async def can_learn(interaction:discord.Interaction,pokemon:str,move_name:int,game_name:str,private:bool=False):
    match=get_close_matches(pokemon,pokedex_dict.keys()) 
    if match is None:
        return await interaction.response.send_message("Could not find that Pokemon.",ephemeral=True)
    pokemon_info=pokedex_dict[match]
    colour=pokemon_info["color"]
    name = pokedex_dict[pokemon]["name"]
    number = pokedex_dict[pokemon]["num"]
    split_game_name = game_name.lower()
    version_num = initial_dict.get(split_game_name, None)
    if version_num is None:
        version_num=get_close_matches(split_game_name,version_dict.keys(),cutoff=0.3)
        if version_num is None:
            raise KeyError("I couldn't find the game you're looking for...")
        split_game_name = version_num.split("-")
        version_num = version_dict[version_num]
    else:
        split_game_name=list(version_dict.keys())[list(version_dict.values()).index(version_num)].split("-")
    pokemon_moveset=deepcopy(movesets[str(number)].get(str(version_num),None))
    pokemon_moveset=await load_movesets_of_pokemon(str(number),str(version_num),None,interaction)
    if pokemon_moveset is None:
        return await interaction.response.send_message("Could not find that pokemon's movesets.",ephemeral=True)
    assert isinstance(pokemon_moveset,dict)
    if pokemon_moveset['1'][0].get("level",None) is None:
        pokemon_moveset=await load_movesets_of_pokemon(number,str(int(version_num)-1),None,interaction)
    if pokemon_moveset is None:
        return await interaction.response.send_message(f"{pokemon.capitalize} didn't exist in {game_name}!",ephemeral=True)
    assert isinstance(pokemon_moveset,dict)
    all_learn_list=[]
    for k,v in pokemon_moveset.items():
        if move_name in (d:=[move['move_id'] for move in v]):
            temp=learn_list_better[int(k)]
            anothertemp=v[d.index(move_name)].get('level',0)
            all_learn_list.append((temp,anothertemp))
    final_move_name=" ".join([e.capitalize() for e in moveid_dict[move_name].split("-")])
    if all_learn_list:
        n='\n'.join(["Method: "+i[0]+('; Level learnt at: '+str(i[1]) if i[1] else '') for i in all_learn_list])
        await interaction.response.send_message(f"{pokemon.capitalize()} learns {final_move_name} in these way(s):\n{n}",ephemeral=private)
    else:
        await interaction.response.send_message(f"{pokemon.capitalize()} does not learn {final_move_name} in any way.",ephemeral=private)
@can_learn.autocomplete("pokemon")
@pokemon_autocomplete
async def can_learn_pokemon_auto(interaction, current):
    ...


@can_learn.autocomplete("game_name")
async def can_learn_gamename_auto(interaction, current):
    return [
        app_commands.Choice(name=e, value=e)
        for e in version_names
        if current.lower() in e.lower()
    ][:25]
@can_learn.autocomplete("move_name")
async def can_learn_move_name_auto(interaction,current):
    return [
        app_commands.Choice(name=" ".join([e.capitalize() for e in k.split("-")]),value=v)
        for k,v in inverse_moveid_dict.items()
        if current.lower().replace(" ","-") in k
    ][:25]
async def setup(bot: Bot):
    # moveset.callback=moveset
    bot.add_command(moveset)
    bot.tree.add_command(can_learn)
    moveset.extras['helpcog'] = bot.cogs["Pokemon"]
    Pokemon.extracommands = [moveset]
