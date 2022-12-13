from lib.bot import Bot
from lib.cogs.pokemon import Pokemon
from discord.ext import commands
from discord import app_commands
from discord.app_commands.
from lib.cogs.pokemon import moveid_dict
import json

with open("lib/cogs/pokedexdata/movesets.json", encoding="utf-8") as move:
    movesets = json.load(move)

@commands.hybrid_command(name="moveset", extras={"url": "movesets"})
@app_commands.describe(
    pokemon="The Pokemon you want to get the moveset of",
    game_name="The game you want to get the moveset of",
    learn_type="The learning method of the moves",
    private="If only you want to see the moveset",
)
async def moveset(
    self,
    ctx,
    pokemon: str = parameter(
        description="The Pokemon you want to see the moveset of."
    ),
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
        raise KeyError(
            "I couldn't find the move learning method you're looking for..."
        )
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
    for d in e:
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
                " ".join(
                    [e.capitalize() for e in moveid_dict[i["move_id"]].split("-")]
                )
            )
            name = f"Level {k}" if k != 0 else "Level not applicable"
        embed.add_field(name=name, value=", ".join(n), inline=False)
    embed = await embed_this_please(ctx, embed)
    return await ctx.send(embed=embed, ephemeral=private)

@moveset.autocomplete("pokemon")
async def moveset_pokemon_auto(self, interaction, current):
    return [
        app_commands.Choice(name=pokemon, value=pokemon)
        for pokemon in pokemon_names_disp
        if current.lower() in pokemon.lower()
    ][:25]

@moveset.autocomplete("game_name")
async def moveset_gamename_auto(self, interaction, current):
    return [
        app_commands.Choice(name=e, value=e)
        for e in version_names
        if current.lower() in e.lower()
    ][:25]

@moveset.autocomplete("learn_type")
async def moveset_learntype_auto(self, interaction, current):
    return [
        app_commands.Choice(name=e.capitalize().replace("-", " "), value=e)
        for e in learn_list.keys()
        if current.lower() in e.lower()
    ][:25]
async def setup(bot:Bot):
    moveset.cog=Pokemon
    await bot.add_command(moveset)