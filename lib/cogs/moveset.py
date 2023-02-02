from lib.bot import Bot
from lib.cogs.pokemon import Pokemon
from discord.ext import commands
from discord import app_commands,Interaction
from discord.ext.commands import parameter
import discord
import difflib
from copy import deepcopy
from typing import Dict, List, Optional

from .pokemon import Pokemon
from .pokemon import moveid_dict, pokedex_dict, embed_this_please, pokemon_names_disp
import ujson
inverse_moveid_dict={}
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
}

with open("lib/cogs/pokedexdata/movesets.json", encoding="utf-8") as move:
    movesets:Dict[str,Dict[str,Dict[str,List[Dict[str,int]]]]] = ujson.load(move)


def with_cog(cog: commands.Cog):
    def inner(command: commands.Command):
        command.helpcog = cog
        return command

    return inner


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
    pokemon: str = parameter(description="The Pokemon you want to see the moveset of."),
    game_name: str = parameter(
        description="The name of the game. Eg. Omega Ruby or use initials like ORAS"
    ),
    learn_type: str = parameter(
        description="The learning method you want to see the moveset of.",
        default="level-up",
    ),
    private: Optional[bool] = parameter(
        description="If only you want to see the moveset. Slash commands only.",
        default=False,
    ),
):
    """Sends the pokemon's moveset in the requested game. See [prefix]help moveset for more info"""
    pokemon = pokemon.lower()
    pokemon = pokemon.replace(" ", "")
    try:
        colour = pokedex_dict[pokemon]["color"]
        name = pokedex_dict["pokemon"]["name"]
        number = pokedex_dict[pokemon]["num"]
    except KeyError:
        try:
            name = difflib.get_close_matches(pokemon, pokedex_dict.keys(), n=1)[0]
            if not len(name):
                return await ctx.send(
                    "Looks like the pokemon you requested doesn't exist..."
                )
            number = pokedex_dict[name]["num"]
            colour = pokedex_dict[name]["color"]
        except:
            return await ctx.send(
                "You've sent an incorrect spelling or a wrong pokemon name"
            )
    game_name = game_name.lower()
    version_num = initial_dict.get(game_name, None)
    if version_num is None:
        version_num = difflib.get_close_matches(
            game_name, version_dict.keys(), n=1, cutoff=0.3
        )
        if not len(version_num):
            raise KeyError("I couldn't find the game you're looking for...")
        game_name = version_num[0].split("-")
        version_num = version_dict[version_num[0]]
    else:
        keys = tuple(version_dict.keys())
        values = tuple(version_dict.values()).index(version_num)
        game_name = keys[values].split("-")
    learn_type_redefined = difflib.get_close_matches(
        learn_type, learn_list.keys(), n=1, cutoff=0.1
    )
    if not len(learn_type_redefined):
        raise KeyError("I couldn't find the move learning method you're looking for...")
    movemethod = learn_type_redefined[0]
    learn_type_redefined = str(learn_list[learn_type_redefined[0]]["id"])
    try:
        e = deepcopy(movesets[str(number)][version_num][learn_type_redefined])
    except:
        return await ctx.send(
            "The Pokemon you sent probably does not exist in that game or it does learn any moves through that method."
        )
    bylevel = {}
    if e[0].get("level", "jfioewjfo") == "jfioewjfo":
        e = deepcopy(
            movesets[str(number)][str(int(version_num) - 1)][learn_type_redefined]
        )
    for d in sorted(e,key=lambda x:x.get('level',1)):
        l = d.get("level", 1)
        ls = bylevel.get(l, [])
        if d.get("level", "jfioewjfo") != "jfioewjfo":
            d.pop("level")
        ls.append(d)
        bylevel.update({l: ls})
    colour = discord.Color.from_rgb(*colour)
    embed = discord.Embed(
        title=name.capitalize(),
        description=f'Move method - {" ".join([e.capitalize() for e in movemethod.split("-")])} \nGame - {", ".join(e.capitalize() if len(e.split())==0 else " ".join([i.capitalize() for i in e.split(" ")]) for e in game_name)}',
        colour=colour,
    )
    for k, v in bylevel.items():
        n = []
        for i in v:
            n.append(
                " ".join([e.capitalize() for e in moveid_dict[i["move_id"]].split("-")])
            )
            name = f"Level {k}" if k != 0 else "Level not applicable"
        embed.add_field(name=name, value=", ".join(n), inline=False)
    embed = await embed_this_please(ctx, embed)
    return await ctx.send(embed=embed, ephemeral=private)


@moveset.autocomplete("pokemon")
async def moveset_pokemon_auto(interaction, current):
    return [
        app_commands.Choice(name=pokemon, value=pokemon)
        for pokemon in pokemon_names_disp
        if current.lower() in pokemon.lower()
    ][:25]


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
@app_commands.command("can_learn")
async def can_learn(interaction:Interaction,pokemon:str,move_name:int,game_name:int):
    pokemon = pokemon.lower()
    pokemon = pokemon.replace(" ", "")
    try:
        colour = pokedex_dict[pokemon]["color"]
        name = pokedex_dict["pokemon"]["name"]
        number = pokedex_dict[pokemon]["num"]
    except KeyError:
        try:
            name = difflib.get_close_matches(pokemon, pokedex_dict.keys(), n=1)[0]
            if not len(name):
                return await interaction.response.send_message(
                    "Looks like the pokemon you requested doesn't exist...",ephemeral=True
                )
            number = pokedex_dict[name]["num"]
            colour = pokedex_dict[name]["color"]
        except:
            return await interaction.response.send_message(
                "You've sent an incorrect spelling or a wrong pokemon name",ephemeral=True
            )
    game_name = game_name.lower()
    version_num = initial_dict.get(game_name, None)
    if version_num is None:
        version_num = difflib.get_close_matches(
            game_name, version_dict.keys(), n=1, cutoff=0.3
        )
        if not len(version_num):
            raise KeyError("I couldn't find the game you're looking for...")
        game_name = version_num[0].split("-")
        version_num = version_dict[version_num[0]]
    else:
        keys = tuple(version_dict.keys())
        values = tuple(version_dict.values()).index(version_num)
        game_name = keys[values].split("-")
    pokemon_moveset=movesets[str(number)].get(str(version_num),None)
    if pokemon_moveset is None:
        return await interaction.response.send_message(f"{pokemon.capitalize} didn't exist in {game_name}!")
    all_learn_list=[]
    for k,v in pokemon_moveset.items():
        if move_name in (d:=[move['move_id'] for move in v]):
            all_learn_list.append((learn_list_better[k],v[d.index(move)].get('level',0)))
    if all_learn_list:
        n='\n'.join([i[0]+(', Level learnt at: '+str(i[1]) if i[1] else '') for i in all_learn_list])
        await interaction.response.send_message(f"{pokemon.capitalize()} learns {moveid_dict[move_name]} in these way(s):{n}")
    else:
        await interaction.response.send_message(f"{pokemon.capitalize()} does not learn {moveid_dict[move_name]} in any way.")
@can_learn.autocomplete("pokemon")
async def can_learn_pokemon_auto(interaction, current):
    return [
        app_commands.Choice(name=pokemon, value=pokemon)
        for pokemon in pokemon_names_disp
        if current.lower() in pokemon.lower()
    ][:25]


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
        app_commands.Choice(name=k,value=v)
        for k,v in inverse_moveid_dict.items()
        if current.lower() in k
    ]
async def setup(bot: Bot):
    # moveset.callback=moveset
    bot.add_command(moveset)
    moveset.helpcog = bot.cogs["Pokemon"]
    Pokemon.extracommands = [moveset]
