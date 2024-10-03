import random
import re
from copy import deepcopy
from typing import List, Optional, Sequence, Tuple

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import parameter

from lib.bot import Bot
from lib.cogs.utils.converters import (
    PokemonConverter,
    SpriteConverter,
    get_close_matches,
)
from lib.cogs.utils import load_files_into_variable
from lib.cogs.utils.autocomplete import pokemon_autocomplete
from ..db import db

type_emoji_dict = {
    "bug": "<:bug:985953221409394759>",
    "dark": "<:dark:985953337256071199>",
    "dragon": "<:dragon:985953408575995914>",
    "electric": "<:electric:985953515681767465>",
    "fairy": "<:fairy:985953654093795338>",
    "fighting": "<:fighting:985953721735323678>",
    "fire": "<:fire:985955119755567125>",
    "flying": "<:flying:985955123303948358>",
    "ghost": "<:ghost:985955415315595284>",
    "grass": "<:grass:985955439734841394>",
    "ground": "<:ground:985955963309813781>",
    "ice": "<:ice:985955967600574525>",
    "normal": "<:normal:985955971094417478>",
    "poison": "<:poison:985955973178986537>",
    "psychic": "<:psychic:985956204993978439>",
    "rock": "<:rock:985956212388548668>",
    "steel": "<:steel:985956509156515920>",
    "water": "<:water:985956512679735328>",
}
back_dict = {
    "afd": "afd-back",
    "none": "ani-back",
    "gen1": "gen1-back",
    "rgb": "gen1rgb-back",
    "gen2": "gen2-back",
    "gen3": "gen3-back",
    "rb": "gen3-back",
    "pt": "gen4-back",
    "bw": "gen5-back",
    "bwani": "gen5ani-back",
}
normal_dict = {
    "bw": "gen5",
    "bwani": "gen5ani",
    "none": "ani",
    "afd": "afd",
    "hgss": "gen4",
    "pt": "gen4dp-2",
    "dp": "gen4dp",
    "gen3": "gen3",
    "rs": "gen3rs",
    "frlg": "gen3frlg",
    "gold": "gen2g",
    "silver": "gen2s",
    "crystal": "gen2",
    "rb": "gen1rb",
    "rg": "gen1rg",
    "yellow": "gen1",
    "gen1": "gen1",
    "gen5": "gen5",
    "gen4": "gen4",
}
type_dict = {
    1: ("Normal", (168, 168, 120)),
    2: ("Fighting", (192, 48, 40)),
    3: ("Flying", (168, 144, 240)),
    4: ("Poison", (160, 64, 160)),
    5: ("Ground", (224, 192, 104)),
    6: ("Rock", (184, 160, 56)),
    7: ("Bug", (168, 184, 32)),
    8: ("Ghost", (112, 88, 152)),
    9: ("Steel", (184, 184, 208)),
    10: ("Fire", (240, 128, 48)),
    11: ("Water", (104, 144, 240)),
    12: ("Grass", (120, 200, 80)),
    13: ("Electric", (248, 208, 48)),
    14: ("Psychic", (248, 88, 136)),
    15: ("Ice", (152, 216, 216)),
    16: ("Dragon", (112, 56, 248)),
    17: ("Dark", (112, 88, 72)),
    18: ("Fairy", (238, 153, 172)),
    10001: ("Unknown", (104, 160, 144)),
    10002: ("Shadow", (104, 160, 144)),
}
colour_dict = {
    "normal": (168, 168, 120),
    "fighting": (192, 48, 40),
    "flying": (168, 144, 240),
    "poison": (160, 64, 160),
    "ground": (224, 192, 104),
    "rock": (184, 160, 56),
    "bug": (168, 184, 32),
    "ghost": (112, 88, 152),
    "steel": (184, 184, 208),
    "fire": (240, 128, 48),
    "water": (104, 144, 240),
    "grass": (120, 200, 80),
    "electric": (248, 208, 48),
    "psychic": (248, 88, 136),
    "ice": (152, 216, 216),
    "dragon": (112, 56, 248),
    "dark": (112, 88, 72),
    "fairy": (238, 153, 172),
    "unknown": (104, 160, 144),
    "shadow": (104, 160, 144),
}
damage_dict = {
    1: "<:status:855828384139051048>",
    2: "<:physical:855828733880303626>",
    3: "<:special:855828580533796864>",
}
target_dict = {
    1: "Specific Move",
    2: "Selected Pokemon or Me First",
    3: "Ally",
    4: "Users side",
    5: "User or Ally",
    6: "Opponents Side",
    7: "User",
    8: "Random Opponent",
    9: "All other Pokemon",
    10: "Selected Pokemon",
    11: "All Opponents",
    12: "Entire Side",
    13: "User and Allies",
    14: "All Pokemon",
    15: "Previous opponent",
    16: "Target and Self"
}
abil_rating_dict = {
    -3: "Absolute Trash",
    -2: "Harmful",
    -1: "Detrimental",
    0: "Useless",
    1: "Ineffective",
    2: "Useful",
    3: "Effective",
    4: "Very Useful",
    5: "Essential",
}

BaseURL = "https://play.pokemonshowdown.com/sprites/"
serebii = "https://www.serebii.net/pokemon/art/"
# Alias cache implementation
location_dict=load_files_into_variable("lib/cogs/pokedexdata/location_dict.json")
location_dict = load_files_into_variable("lib/cogs/pokedexdata/location_dict.json")
evol_lines = load_files_into_variable("lib/cogs/pokedexdata/pokemon_evolution_lines.json")
types=load_files_into_variable("lib/cogs/pokedexdata/typechart.json")
pokedex_dict=load_files_into_variable("lib/cogs/pokedexdata/pokemon_stuff_english_only.json")
moves_dict=load_files_into_variable("lib/cogs/pokedexdata/nonexistentfile.json")
move_names: Tuple[str,...] = tuple(moves_dict.keys())
evol_dict=load_files_into_variable("lib/cogs/pokedexdata/pokemon_evolutions.json")
abil_flav_dict=load_files_into_variable("lib/cogs/pokedexdata/abilities_flavour_text_english_only.json")
abil_stuff_dict=load_files_into_variable("lib/cogs/pokedexdata/ability_stuff.json")
abil_names: Tuple[str,...] = tuple(v["name"] for v in abil_stuff_dict.values())
item_stuff_dict=load_files_into_variable("lib/cogs/pokedexdata/item_names_and_flavour_combined_english.json")
item_id_dict=load_files_into_variable("lib/cogs/pokedexdata/item_names_english_only.json")
item_names = tuple(name for name in item_id_dict.values())

id_dict = {}
for k, v in pokedex_dict.items():
    if id_dict.get(str(v["num"]), None) is None:
        id_dict[str(v["num"])] = (k, v["name"])
moveid_dict = {}
for k, v in moves_dict.items():
    idnumber = v["id"]
    moveid_dict[idnumber] = k
PokedexConverter = PokemonConverter(list(pokedex_dict.keys()), True)

SPRITE_REGEX = re.compile(
    r"(^|\s)(\*|_)(?P<name>[a-zA-Z0-9-][a-zA-Z0-9 -]*)(\2| |\Z)",
    flags=re.IGNORECASE,
)

messages = [
    "Support our bot's journey! Write a review and vote on [Top.gg](https://top.gg/bot/853556227610116116) now!",
]


async def add_info_to_embed(ctx: commands.Context[Bot], embed: discord.Embed):
    if random.randint(1, 20) == 1:
        embed.add_field(
            name="**We really hope you're enjoying the bot...**",
            value=messages[0],
        )

    if ctx.interaction is None and ctx.guild is None:
        embed.set_footer(
            text=f"Did you know that you can also use the slash command and set private = True so nobody else can see it?"
        )
    return embed


async def get_pokedex_stuff(pokemon_dict, lite=False):
    stats = []
    total = 0
    stats_dict = pokemon_dict["baseStats"]
    for stat_name, value in stats_dict.items():
        stats.append(f"**{stat_name}**: {value}")
        total = total + value
    stats.append(f"**Total**: {total}")
    stats = ", ".join(stats)
    # fourth field is the stats
    abilities_dict = pokemon_dict["abilities"]
    abilities = []
    for type, value in abilities_dict.items():
        try:
            if type == "H":
                value = "*" + value.capitalize() + "*"
        except:
            pass
        abilities.append(value)
    if len(abilities) == 1:
        Abilities = "Ability"
    else:
        Abilities = "Abilities"
    abilities = ", ".join(abilities)
    if not lite:
        types = ", ".join(pokemon_dict["types"])
        if len(pokemon_dict["types"]) == 1:
            multipleTypes = "Type"
        else:
            multipleTypes = "Types"
        name = " ".join(
            n.capitalize() for n in pokemon_dict["name"].replace("-", " ").split()
        )
        # name:str=name.replace("-"," ")
        # name=" ".join(n.capitalize() for n in name.split())
        colour: Sequence[int] = pokemon_dict["color"]
        if not isinstance(colour, list):
            colour = (88, 101, 242)
        # Title is the name
        try:
            dex_entry = random.choice(pokemon_dict["flavourText"])
        except KeyError:
            try:  # Temporary fix to the swsh pokemon not having dex entries
                dex_entry = random.choice(
                    pokedex_dict[pokemon_dict["baseSpecies"].lower()]["flavourText"]
                )
            except:
                dex_entry = ""
        if dex_entry != "":
            embed = discord.Embed(
                title=name,
                description=f"*{dex_entry}*",
                colour=discord.Color.from_rgb(*colour),
            )
        # then the next field is the types
        else:
            embed = discord.Embed(title=name, colour=discord.Color.from_rgb(*colour))
        embed.add_field(name=f"**{multipleTypes}**", value=f"{types}", inline=True)

        try:
            genderRatio = pokemon_dict["genderRatio"]
            genderlist = []
            for gender_name, value in genderRatio.items():
                genderlist.append(f"{gender_name}: {value * 100}%")
            genderRatio = "\n".join(genderlist)
        except KeyError:
            try:
                # There's no gender ratio therefore its no gender or 100% female or male
                genderRatio = pokemon_dict["gender"]
                genderRatio = (
                    "No Gender"
                    if genderRatio == "N"
                    else "Male"
                    if genderRatio == "M"
                    else "Female"
                )
            except KeyError:
                genderRatio = "M: 50%, F: 50%"
        if genderRatio != "":
            # third field is gender
            embed.add_field(
                name="**Gender Percentage**", value=f"{genderRatio}", inline=True
            )
        embed.add_field(name="**Stats**", value=f"{stats}", inline=False)

        # The entire evolution check depends on the fact that there are no 4 chain evolutions
        try:
            # Try checking if the first evolution exists. For example , Psyduck to Golduck
            firstevo = pokemon_dict["evos"]
            EvoString = "**" + name.capitalize() + "**" + " → " + firstevo[0]
            try:
                secondevo = (pokedex_dict[f"{firstevo[0].lower()}"])["evos"]
                EvoString = (
                    "**"
                    + name.capitalize()
                    + "**"
                    + " → "
                    + firstevo[0]
                    + " → "
                    + secondevo[0]
                )
            except KeyError:
                try:
                    pre_evo = pokemon_dict["prevo"]
                    EvoString = (
                        pre_evo
                        + " → "
                        + "**"
                        + name.capitalize()
                        + "**"
                        + " → "
                        + firstevo[0]
                    )
                except:
                    pass
        except KeyError:
            # A first evolution doesn't exist which eliminates the possiblity of a third evolution too
            try:
                # Try checking if the pokemon has a pre evolution , example- Furret <-- Sentret
                pre_evo = pokemon_dict["prevo"]
                EvoString = pre_evo + " → " + "**" + name.capitalize() + "**"
                try:
                    # The pokemon has a pre evolution.
                    # Try checking if the pokemon has a first evolution (Egg form) . Example -
                    pre_evo_of_pre_evo = (pokedex_dict[f"{pre_evo.lower()}"])["prevo"]
                    EvoString = (
                        pre_evo_of_pre_evo
                        + " → "
                        + pre_evo
                        + " → "
                        + "**"
                        + name.capitalize()
                        + "**"
                    )
                except:
                    # The pokemon is lonely like dunsparce with no evolutions before or after.
                    pass
            except:
                EvoString = ""
                pass
        if EvoString != "":
            embed.add_field(name="**Evolution**", value=f"{EvoString}", inline=False)

        url = pokemon_dict.get("url", "")
        if len(pokemon_dict["eggGroups"]) == 1:
            Egg = "Egg Group"
        else:
            Egg = "Egg Groups"

        embed.set_thumbnail(url=serebii + url + ".png")
        embed.insert_field_at(
            2, name=f"**{Abilities}**", value=f"{abilities}", inline=True
        )
        height = pokemon_dict["heightm"]
        weight = pokemon_dict["weightkg"]
        tier = pokemon_dict.get("Tier", None)
        if tier is None:
            tier = pokedex_dict.get(
                pokemon_dict.get("baseSpecies","").lower().replace("-", ""), {}
            ).get("Tier", "None")
        urllist = []
        try:
            name = pokemon_dict["baseSpecies"]
        except KeyError:
            pass
        if pokemon_dict["num"] <= 0:
            name = (name.replace(" ", "-")).lower()
            urllist.append(f"[Smogon](https://www.smogon.com/dex/sv/pokemon/{name})")
        else:
            name = name.replace(" ", "_")
            urllist.append(
                f"[Bulbapedia](https://bulbapedia.bulbagarden.net/wiki/{name})"
            )
            newname = (name.replace("_", "-").replace(".", "")).lower()
            urllist.append(f"[PokemonDB](https://pokemondb.net/pokedex/{newname})")
            urllist.append(
                f"[Smogon](https://www.smogon.com/dex/sv/pokemon/{newname}/)"
            )
            urllist.append(
                f"[Serebii](https://www.serebii.net/pokemon/{name.replace('_','').lower()})"
            )
        embed.add_field(name="**Height**", value=f"{height}m", inline=False)
        embed.add_field(name="**Weight**", value=f"{weight}kg", inline=True)
        embed.add_field(name="**Smogon Tier**", value=tier, inline=True)
        embed.add_field(
            name=f"**{Egg}**",
            value=f"{', '.join(pokemon_dict['eggGroups'])}",
            inline=False,
        )
        embed.add_field(
            name="**External Resources**", value=f"{' • '.join(urllist)}", inline=False
        )
        return embed
    else:
        embed = discord.Embed(
            title=" ".join(
                n.capitalize() for n in pokemon_dict["name"].replace("-", " ").split()
            ),
            colour=discord.Color.from_rgb(*pokemon_dict["color"])
            if isinstance(pokemon_dict["color"], (list, tuple))
            else discord.Color.blurple(),
        )
        types = ", ".join(pokemon_dict["types"])
        if len(pokemon_dict["types"]) == 1:
            multipleTypes = "Type"
        else:
            multipleTypes = "Types"
        try:
            embed.set_thumbnail(url=serebii + pokemon_dict["url"] + ".png")
        except:
            pass
        embed.add_field(name="**Types**", value=types, inline=False)
        embed.add_field(name="**Abilities**", value=abilities, inline=True)
        embed.add_field(name="**Stats**", value=stats, inline=False)
        return embed


async def convert_move_to_embed(name, move_provided, flavourmmm):
    power: int = move_provided["power"]
    accuracy: str = str(move_provided["accuracy"])
    if accuracy != "None":
        accuracy += "%"
    pp: int = move_provided["pp"]
    title: str = damage_dict[move_provided["damage_class_id"]] + " " + name
    if isinstance((n := move_provided["generation_id"]), int):
        flavourmmm = flavourmmm + f"\n*Generation introduced: {n}*"
    embed = discord.Embed(
        title=title,
        description=flavourmmm,
        colour=discord.Color.from_rgb(*(type_dict[move_provided["type_id"]])[1]),
    )
    embed.add_field(
        name="Type", value=f"{type_dict[move_provided['type_id']][0]}", inline=True
    )
    embed.add_field(name="PP", value=f"{pp}", inline=True)
    embed.add_field(name="Base Power", value=f"{power}", inline=True)
    embed.add_field(name="Accuracy", value=f"{accuracy}", inline=True)
    embed.add_field(
        name="Target", value=f"{target_dict[move_provided['target_id']]}", inline=True
    )
    embed.add_field(name="Priority", value=f"{move_provided['priority']}", inline=True)
    return embed


async def convert_four_baseurl(
    back: bool, shiny: bool, pokemon: str, sprite_type: str, ctx: commands.Context
):
    if back:
        try:
            url = back_dict[sprite_type]
            if (
                shiny
                and "gen2g" not in url
                and "gen1" not in url
                and "gen2s" not in url
            ):
                url = url + "-shiny"
            url = url + "/" + pokemon + (".gif" if "ani" in url else ".png")
        except KeyError:
            raise KeyError("That sprite type was not found for back sprites...")
    else:
        try:
            url = normal_dict[sprite_type]
            if (
                shiny
                and "gen2g" not in url
                and "gen1" not in url
                and "gen2s" not in url
            ):
                url = url + "-shiny"
            url = url + "/" + pokemon + (".gif" if "ani" in url else ".png")
        except KeyError:
            raise KeyError(
                f"Couldn't find that sprite type... Try seeing {ctx.prefix}help sprite for all the available sprite types..."
            )
    return url


class Pokemon(commands.Cog):
    """All of the Pokemon related commands"""
    extracommands:List=[]
    url = "pokemon-related-commands"


    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.group(extras={"url": "alias-management"})
    async def alias(self, ctx: commands.Context):
        """Alias commands for sprites"""
        if ctx.invoked_subcommand is None:
            pass

    @alias.command(
        name="add", extras={"url": "span-stylecoloryellowhow-to-add-an-alias-span"}
    )
    @commands.has_permissions(manage_guild=True)
    async def add_alias(
        self,
        ctx: commands.Context,
        alias: str = parameter(description="The text that will call the sprite."),
        *,
        sprite: SpriteConverter = parameter(
            description="The sprite that will be called via the alias."
        ),
    ):
        """Adds an alias to a sprite for easy access and memes"""
        assert (
            ctx.guild is not None and self.bot.alias_cache is not None
        )  # Command can only be used in guilds due to the permission check
        alias = alias.lower()
        back, shiny, sprite_type, pokemon = sprite
        url = await convert_four_baseurl(back, shiny, pokemon, sprite_type.lower(), ctx)
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url=BaseURL + url) as r:
                if r.status != 200:
                    raise KeyError("The sprite is not available in that format...")
        await db.insert_new_alias(
            ctx.guild.id,
            alias,
            f"{pokemon} {sprite_type if sprite_type!='none' else ''} {'back' if back else ''} {'shiny' if shiny else ''}".strip(),
        )
        await ctx.message.add_reaction("✅")

    @alias.command(
        name="remove",
        extras={"url": "span-stylecoloryellowhow-to-remove-an-alias-span"},
    )
    @commands.has_permissions(manage_guild=True)
    async def remove_alias(
        self, ctx, alias: str = parameter(description="The alias to remove.")
    ):
        """Removes an existing alias"""
        await db.remove_alias(ctx.guild.id, alias)
        await ctx.message.add_reaction("✅")

    @alias.command(
        name="list", extras={"url": "span-stylecoloryellowhow-to-list-all-aliases-span"}
    )
    async def list_aliases(self, ctx):
        """Lists all the server aliases for a pokemon"""
        aliases = await db.alias_cache[ctx.guild.id]
        assert isinstance(aliases, tuple)
        all_aliases = []
        for n, (e, v) in enumerate(zip(*aliases), start=1):
            if e or v:
                all_aliases.append(f"{n} : `{e}` ➔ `{v}`")
        if not all_aliases:
            return await ctx.send("You do not have any aliases set for this server!")
        embed = discord.Embed(
            title=f"Aliases for this server ({ctx.guild.name})",
            description="\n".join(all_aliases),
            colour=discord.Color.blurple(),
        )

        await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="ability", aliases=["abil"], extras={"url": "abilities"}
    )
    @app_commands.describe(
        ability="The ability you want to get information on",
        private="If only you want to see the info.",
    )
    async def ability(
        self,
        ctx: commands.Context,
        *,
        ability: str = parameter(description="The ability name to see info on"),
        private: Optional[bool] = parameter(
            description="If only you want to see the info. (Only slash commands)",
            default=False,
        ),
    ):
        """Sends information about the ability"""
        ability = ability.lower()
        ability = ability.replace(" ", "")
        try:
            abil_dict = abil_stuff_dict[ability]
        except KeyError:
            name = get_close_matches(ability, abil_stuff_dict.keys())
            if name is None:
                return await ctx.send(
                    "Looks like the ability you requested doesn't exist..."
                )
            abil_dict = abil_stuff_dict[name]
        name = abil_dict["name"]
        urldict = []
        underscorename = name.replace(" ", "_")
        urldict.append(
            f"[Bulbapedia](https://bulbapedia.bulbagarden.net/wiki/{underscorename}_(Ability%29)"
        )
        hyphenname = name.replace(" ", "-")
        urldict.append(f"[PokemonDB](https://pokemondb.net/ability/{hyphenname})")
        urldict.append(
            f"[Smogon](https://www.smogon.com/dex/sv/abilities/{hyphenname}/)"
        )
        nospacesname = (name.replace(" ", "")).lower()
        urldict.append(
            f"[Serebii](https://www.serebii.net/abilitydex/{nospacesname}.shtml)"
        )
        flavourText = abil_dict.get("flavourText", None)
        if flavourText is None:
            flavourText = abil_flav_dict.get(str(abil_dict["num"]), "No flavour text")
            if isinstance(flavourText, list):
                flavourText = flavourText[-1]
        embed = discord.Embed(
            title=abil_dict["name"],
            description=flavourText,
            colour=discord.Color.blurple(),
        )
        embed.add_field(
            name="Smogon Rating",
            value=f"{abil_rating_dict[int(abil_dict['rating'])]} ({abil_dict['rating']})",
            inline=True,
        )
        embed.add_field(
            name="External Resources", value=f'{" • ".join(urldict)}', inline=False
        )
        embed = await add_info_to_embed(ctx, embed)
        if private is None:
            private = False
        await ctx.send(embed=embed, ephemeral=private)

    @ability.autocomplete("ability")
    async def abil_auto(self, interaction: discord.Interaction, current: str):
        return [
            app_commands.Choice(name=ability, value=ability)
            for ability in abil_names
            if current.lower() in ability.lower()
        ][:25]

    @commands.command(
        name="type", aliases=["weak"], extras={"url": "type-matchup-calculations"}
    )
    async def type(
        self,
        ctx: commands.Context,
        *,
        pokemon_or_move_or_typestring: str = parameter(
            description="The Pokemon name or the move name or the type(s) to see the matchup on"
        ),
    ):
        """Sends the information about the requested type/(pokemon's/move's) types
        Can only send two types at maximum"""
        pokemon_or_move_or_typestring = pokemon_or_move_or_typestring.lower()
        supereffectiveFrom = []
        effectiveFrom = []
        resistantFrom = []
        immuneFrom = []
        supereffectiveTo = []
        effectiveTo = []
        resistantTo = []
        immuneTo = []
        image_link = ""
        name = ""
        try:
            [types[e]["damageTaken"] for e in pokemon_or_move_or_typestring.split()]
            if len(pokemon_or_move_or_typestring.split()) > 2:
                return await ctx.send("You can't send more than two types.")
        except KeyError:
            try:
                name = await PokedexConverter.convert(
                    ctx, pokemon_or_move_or_typestring
                )
                pokemon_or_move_or_typestring = " ".join(
                    pokedex_dict[name]["types"]
                ).lower()
                image_link = pokedex_dict[name].get("url", "")
                if image_link:
                    image_link = f"https://www.serebii.net/pokemon/art/{image_link}.png"
            except KeyError:
                name = get_close_matches(
                    pokemon_or_move_or_typestring, moves_dict.keys()
                )
                if name is None:
                    return await ctx.send(
                        "I couldn't match your input to a type or pokemon or move"
                    )
                pokemon_or_move_or_typestring = type_dict[moves_dict[name]["type_id"]][
                    0
                ].lower()

        for two in pokemon_or_move_or_typestring.split():
            typetobeseen = types[two]["damageTaken"]
            for v, e in typetobeseen.items():
                if e == 1:
                    supereffectiveFrom.append(v)
                elif e == 0:
                    effectiveFrom.append(v)
                elif e == 2:
                    resistantFrom.append(v)
                else:
                    immuneFrom.append(v)
            two = two.capitalize()
            for k, v in types.items():
                k = k.capitalize()
                v = v["damageTaken"]
                if v[two] == 1:
                    supereffectiveTo.append(k)
                elif v[two] == 0:
                    effectiveTo.append(k)
                elif v[two] == 2:
                    resistantTo.append(k)
                else:
                    immuneTo.append(k)
        if len(pokemon_or_move_or_typestring.split()) > 1:
            for e in immuneFrom:
                if e in supereffectiveFrom:
                    supereffectiveFrom.remove(e)
            neweffectiveFrom = effectiveFrom.copy()
            for e in neweffectiveFrom:
                if e in supereffectiveFrom:
                    effectiveFrom.remove(e)
                elif e in immuneFrom:
                    effectiveFrom.remove(e)
                elif e in resistantFrom:
                    effectiveFrom.remove(e)
            newresistantfrom = resistantFrom.copy()
            for e in newresistantfrom:
                if e in supereffectiveFrom:
                    effectiveFrom.append(e)
                    supereffectiveFrom.remove(e)
                    resistantFrom.remove(e)
            newresistantfrom = resistantTo.copy()

        if len(pokemon_or_move_or_typestring.split()) > 1:
            if len(set(supereffectiveFrom)) != len(supereffectiveFrom):
                repeatedTypes = [
                    x for x in supereffectiveFrom if supereffectiveFrom.count(x) > 1
                ]
                for e in set(repeatedTypes):
                    supereffectiveFrom.remove(e)
                    ind = supereffectiveFrom.index(e)
                    supereffectiveFrom[ind] = f"**__{supereffectiveFrom[ind]}__**"
            if len(set(resistantFrom)) != len(resistantFrom):
                repeatedTypes = [x for x in resistantFrom if resistantFrom.count(x) > 1]
                for e in set(repeatedTypes):
                    resistantFrom.remove(e)
                    ind = resistantFrom.index(e)
                    resistantFrom[ind] = "__**" + resistantFrom[ind] + "**__"
        if name:
            name = name.replace("-", " ")
            # name=[name] if type(name)==str else name
            name = name.split()
            name = " " + " ".join(n.capitalize() for n in name)
        else:
            name = ""
        emojis = "".join(
            [type_emoji_dict[e] for e in pokemon_or_move_or_typestring.split()]
        )
        embed = discord.Embed(
            title=emojis + name,
            colour=discord.Color.from_rgb(*colour_dict[two.lower()]),  # type:ignore
            description=", ".join(
                [e.capitalize() for e in pokemon_or_move_or_typestring.split()]
            ),
        )
        embed.add_field(
            name="**__DEFENSE__**\n\n *Weak to:*",
            value=", ".join(dict.fromkeys(supereffectiveFrom))
            if supereffectiveFrom
            else "None",
            inline=False,
        )
        embed.add_field(
            name="*Takes normal damage from:* ",
            value=", ".join(dict.fromkeys(effectiveFrom)) if effectiveFrom else "None",
            inline=False,
        )
        embed.add_field(
            name="*Resists:*",
            value=", ".join(dict.fromkeys(resistantFrom)) if resistantFrom else "None",
            inline=False,
        )
        embed.add_field(
            name="*Is Immune to:*",
            value=", ".join(dict.fromkeys(immuneFrom)) if immuneFrom else "None",
            inline=False,
        )

        ##OFFENSIVE
        if len(pokemon_or_move_or_typestring.split()) == 1:
            embed.add_field(
                name="**__OFFENSE__**\n\n *Does super effective damage to:*",
                value=", ".join(dict.fromkeys(supereffectiveTo))
                if supereffectiveTo
                else "None",
                inline=False,
            )
            if effectiveTo:
                embed.add_field(
                    name="*Deals normal damage to:* ",
                    value=", ".join(dict.fromkeys(effectiveTo))
                    if effectiveTo
                    else "None",
                    inline=False,
                )
            if resistantTo:
                embed.add_field(
                    name="*Resisted by:*",
                    value=", ".join(dict.fromkeys(resistantTo))
                    if resistantTo
                    else "None",
                    inline=False,
                )
            if immuneTo:
                embed.add_field(
                    name="*Does not affect:*",
                    value=", ".join(dict.fromkeys(immuneTo)) if immuneTo else "None",
                    inline=False,
                )
        embed = await add_info_to_embed(ctx, embed)
        if image_link:
            embed.set_thumbnail(url=image_link)
        embed.set_footer(text="Bolded underline indicates double weakness/resistance")
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="item", extras={"url": "items"})
    @app_commands.describe(
        itemname="The item you want to get information on",
        private="If only you want to see the info.",
    )
    async def iteminfo(
        self,
        ctx,
        *,
        itemname: str = parameter(description="The name of the item."),
        private: Optional[bool] = parameter(
            description="If only you want to see the info. (Only slash commands))",
            default=False,
        ),
    ):
        """Sends info about the item"""
        itemname = itemname.lower()
        itemname = itemname.replace(" ", "")
        close_itemname = get_close_matches(itemname, item_names)
        if close_itemname is None:
            return await ctx.send(
                "You've sent an incorrect spelling or a wrong item name"
            )
        item_dict = item_stuff_dict[close_itemname]
        flavour_text_item = item_dict["FlavourText"]
        sprite = item_dict["sprite"]
        embed = discord.Embed(
            title=f"{close_itemname}",
            description=f"{flavour_text_item[-1]}",
            colour=discord.Color.blurple(),
        )
        if sprite:
            embed.set_thumbnail(url=sprite)
        itemname = itemname.replace("é", "e")
        underscorename = itemname.replace(" ", "_")
        hyphenlink = itemname.replace(" ", "-")

        urllist = []
        urllist.append(
            f"[Bulbapedia](https://bulbapedia.bulbagarden.net/wiki/{underscorename})"
        )
        urllist.append(f"[PokemonDB](https://pokemondb.net/item/{hyphenlink.lower()})")
        urllist.append(
            f"[Smogon](https://www.smogon.com/dex/sv/items/{hyphenlink.lower()}/)"
        )
        nospacelink = itemname.replace(" ", "")
        urllist.append(
            f"[Serebii](https://www.serebii.net/itemdex/{nospacelink.lower()}.shtml)"
        )

        embed.add_field(
            name="External Resources", value=f"{' • '.join(urllist)}", inline=False
        )
        embed = await add_info_to_embed(ctx, embed)
        await ctx.send(embed=embed, ephemeral=private)

    @iteminfo.autocomplete("itemname")
    async def auto_item(self, interaction: discord.Interaction, current: str):
        return [
            app_commands.Choice(name=item, value=item)
            for item in item_names
            if current.lower() in item.lower()
        ][:25]

    @commands.command(name="sprite", aliases=["sp"], extras={"url": "sprites"})
    async def sprite(
        self,
        ctx: commands.Context,
        *,
        sprite_name: SpriteConverter = parameter(
            description="The Pokemon you want to see the sprite of. Find a more detailed guide in the wiki."
        ),
    ):
        """Sends the requested sprite. See [prefix]help sprite for more info.
        pokemon : Pokemon name
        sprite_type : Check the wiki for a detailed guide
        Note: gmax and mega can be done by <pokemon>-gmax and <pokemon>-mega\n"""
        back, shiny, sprite_type, pokemon = sprite_name  # type:ignore
        if pokemon.lower() == "dab":
            embed = discord.Embed()
            embed.set_image(
                url="https://cdn.discordapp.com/attachments/777782956357320714/868583991031234590/kadabra.png"
            )
            return await ctx.send(embed=embed)
        url = await convert_four_baseurl(back, shiny, pokemon, sprite_type, ctx)
        embed = discord.Embed()
        embed.set_image(url=BaseURL + url)
        # embed=await embed_this_please(ctx,embed)
        return await ctx.send(embed=embed)

    # @app_commands.command(name='sprite',description='Sends the ingame sprite of the requested Pokemon',extras={"url":"sprites"})
    # async def sprite_slash(self,interaction:discord.Interaction,pokemon:str,version_name:Optional[str],back:Optional[bool]=False,shiny:Optional[bool]=False,private:Optional[bool]=False):
    #     await interaction.response.send_message("amogus sussy imposter",ephemeral=True)

    # @sprite_slash.autocomplete("pokemon")
    # async def sprite_autopokemon(self,interaction,current):
    #     return []
    @commands.hybrid_command(name="pokedex", aliases=["dex"], extras={"url": "pokedex"})
    @app_commands.describe(
        pokemon="The Pokemon you want to get information on",
        private="If only you want to see the info.",
        lite="If you want to get lightweight info.",
    )
    async def pokedex(
        self,
        ctx: commands.Context,
        *,
        pokemon: PokedexConverter = parameter(  # type:ignore
            description="The Pokemon you want to see the info on."
        ),
        private: Optional[bool] = parameter(
            description="If only you want to see the info.", default=False
        ),
        lite: bool = False,
    ):
        """Sends dex information about the pokemon"""

        pokemon_dict = pokedex_dict[pokemon]
        embed = await get_pokedex_stuff(pokemon_dict, lite)
        embed = await add_info_to_embed(ctx, embed)
        if private is None:
            private = False
        await ctx.send(embed=embed, ephemeral=private)

    @pokedex.autocomplete("pokemon")
    @pokemon_autocomplete
    async def auto_dex(self, interaction, current: str):
        ...

    @commands.hybrid_command(
        name="ldex", aliases=["litedex", "cheapdex"], extras={"url": "lite-pokedex"}
    )
    @app_commands.describe(
        pokemon="The Pokemon you want to get information on",
        private="If only you want to see the info.",
    )
    async def lite_dex(
        self,
        ctx,
        *,
        pokemon: PokedexConverter = parameter(  # type:ignore
            description="The Pokemon you want to see the info on."
        ),
        private: Optional[bool] = parameter(
            description="If only you want to see the info.", default=False
        ),
    ):
        """Sends light weight information about the pokemon"""
        pokemon_dict = pokedex_dict[pokemon]
        embed = await get_pokedex_stuff(pokemon_dict, True)
        embed = await add_info_to_embed(ctx, embed)
        await ctx.send(embed=embed, ephemeral=private)

    @lite_dex.autocomplete("pokemon")
    @pokemon_autocomplete
    async def auto_ldex(self, interaction, current: str):
        ...

    @commands.hybrid_command(
        name="artwork", aliases=["art"], extras={"url": "artworks"}
    )
    @app_commands.describe(
        pokemon="The Pokemon you want to get the artwork of",
        private="If only you want to see the artwork",
    )
    async def artwork(
        self,
        ctx,
        *,
        pokemon: PokedexConverter = parameter(  # type:ignore
            description="The Pokemon you want to see the artwork of."
        ),
        private: Optional[bool] = parameter(
            description="If only you want to see the artwork. Only slash commands.",
            default=False,
        ),
    ):
        """Sends the official artwork of the mentioned pokemon"""
        url = pokedex_dict[pokemon].get("url", None)
        if url is None:
            raise TypeError("I couldn't find the artwork for that Pokemon")
        embed = discord.Embed()
        embed.set_image(url=serebii + url + ".png")
        # embed.set_footer(text="Please report any wrong artworks using the `feedback` command!")
        embed = await add_info_to_embed(ctx, embed)
        await ctx.send(embed=embed, ephemeral=private)

    @artwork.autocomplete("pokemon")
    @pokemon_autocomplete
    async def auto_artwork(self, interaction, current: str):
        ...

    @commands.hybrid_command(name="move", extras={"url": "moves"})
    @app_commands.describe(
        move="The move you want to get information on",
        private="If only you want to see the info.",
    )
    async def moveinfo(
        self,
        ctx,
        *,
        move: str = parameter(description="The move you want to see the info on."),
        private: Optional[bool] = parameter(
            description="If only you want to see it. Only slash commands.",
            default=False,
        ),
    ):
        """Sends move info about the requested move"""
        move = move.lower()
        move = move.replace(" ", "")
        try:
            move_dict = moves_dict[move]
            name = move
        except KeyError:
            name = get_close_matches(move, moves_dict.keys())
            if name is None:
                return await ctx.send(
                    "Looks like the move you requested doesn't exist..."
                )
            move_dict = moves_dict[name]

        urllist = []
        newname = []
        name = name.split("-")
        for i in name:
            if i in ["of"]:
                newname.append(i)
            else:
                newname.append(i.capitalize())
        name = " ".join(newname)
        underscorename = name.replace(" ", "_")
        urllist.append(
            f"[Bulbapedia](https://bulbapedia.bulbagarden.net/wiki/{underscorename}_(move%29)"
        )
        hyphenname = (name.replace(" ", "-")).lower()
        urllist.append(f"[PokemonDB](https://pokemondb.net/move/{hyphenname})")
        urllist.append(f"[Smogon](https://www.smogon.com/dex/sv/moves/{hyphenname}/)")
        flavourmmm = move_dict.get("flavourText", ["Could not find flavour text."])[-1]
        nospacename = (name.replace(" ", "")).lower()
        if (
            flavourmmm
            == "This move can\u2019t be used. It\u2019s recommended that this move is forgotten. Once forgotten, this move can\u2019t be remembered."
        ):
            flavourmmm = move_dict["flavourText"][-2]
            urllist.append(
                f"[Serebii](https://www.serebii.net/attackdex-sm/{nospacename}.shtml)"
            )
        else:
            urllist.append(
                f"[Serebii](https://www.serebii.net/attackdex-swsh/{nospacename}.shtml)"
            )
        if not flavourmmm:
            flavourmmm = "\u200b"
        urllist.append(
            f"[Showdown!](https://dex.pokemonshowdown.com/moves/{nospacename})"
        )
        embed = await convert_move_to_embed(name, move_dict, flavourmmm)
        embed.add_field(
            name="External Resources", value=" • ".join(urllist), inline=False
        )
        embed = await add_info_to_embed(ctx, embed)
        await ctx.send(embed=embed, ephemeral=private)

    @moveinfo.autocomplete("move")
    async def auto_move(self, interaction, current: str):
        return [
            app_commands.Choice(name=move.replace("-", " ").capitalize(), value=move)
            for move in move_names
            if current.lower() in move.lower()
        ][:25]

    @commands.hybrid_command(
        name="evo", aliases=["evolution", "evol"], extras={"url": "evolution-chains"}
    )
    @app_commands.describe(
        pokemon="The Pokemon you want to get the evolution chain on",
        private="If only you want to see the info.",
    )
    async def evolution(
        self,
        ctx: commands.Context,
        *,
        pokemon: PokedexConverter = parameter(  # type:ignore
            description="The Pokemon you want to see the evolution chain of."
        ),
        private: Optional[bool] = parameter(
            description="If only you want to see it. Slash commands only.",
            default=False,
        ),
    ):
        """Fetch the evolution chain of a Pokemon"""

        pokemon_id = pokedex_dict[pokemon]["num"]
        colour = pokedex_dict[pokemon]["color"]
        if pokemon_id <= 0:
            return await ctx.send("Fakemons aren't available")
        if pokemon_id >= 899:
            return await ctx.send(
                "Sorry, but only Pokemon till Generation 8 (SwSh) are supported.\nThe developer does not plan to add the latest Pokemon's evolutions due to the various different complicated evolution lines introduced."
            )
        try:
            evol_line = evol_lines[str(pokemon_id).lower()]
        except KeyError:
            return await ctx.send("That Pokemon doesn't have an evolution!")
        all_stuff = [deepcopy(evol_dict[d]) for d in evol_line[1:]]
        evol_line_but_keys = [id_dict[e][0] for e in evol_line]
        evol_line = [id_dict[e][1] for e in evol_line]
        embed = discord.Embed(
            title="Evolution Chain", colour=discord.Color.from_rgb(*colour)
        )
        for i, hmm in enumerate(all_stuff):
            hmm = hmm[0]
            evolves_to = evol_line[i + 1]
            evolves_from = pokedex_dict[evol_line_but_keys[i + 1]]["prevo"]
            hmm: dict = hmm
            overworld_rain = False
            upside_down = False
            trig_id = hmm["evolution_trigger_id"]
            if hmm["needs_overworld_rain"]:
                overworld_rain = True
            elif hmm["turn_upside_down"]:
                upside_down = True
            hmm.pop("evolution_trigger_id")
            hmm.pop("needs_overworld_rain")
            hmm.pop("id")
            hmm.pop("turn_upside_down")
            l = []
            if trig_id == 1:
                l = ["Level up and"]
                for k, v in hmm.items():
                    if k == "relative_physical_stats":
                        if v == 0:
                            l.append("Attack Stat=Defense Stat")
                        elif v > 0:
                            l.append("Attack Stat>Defense Stat")
                        elif v < 0:
                            l.append("Attack Stat<Defense Stat")
                    elif k == "minimum_level":
                        l.append(f"Minimum level needs to be {v}")
                    elif k == "minimum_happiness":
                        l.append(f"Minimum happiness has to be {v}")
                    elif k == "known_move_id":
                        move: str = moveid_dict[v]
                        move = move.replace("-", " ")
                        move = move.capitalize()
                        l.append(f"Should know move - {move}")
                    elif k == "minimum_beauty":
                        l.append(f"Minimum beauty needs to be {v}")
                    elif k == "minimum_affection":
                        l.append(f"Minimum affection needs to be {v}")
                    elif k == "time_of_day":
                        l.append(f"Time of day has to be {v.capitalize()}")
                    elif k == "location_id":
                        l.append(f"Location has to be {location_dict[str(v)]}")
                    elif k == "gender_id":
                        l.append(f"Gender has to be {'Male' if v==2 else 'Female'}")
                    elif k == "known_move_type_id":
                        l.append(f"The Pokemon should know a {type_dict[v][0]} move")
                    elif k == "held_item_id":
                        name = (item_id_dict[str(v)]).capitalize()
                        name = name.replace("-", " ")
                        l.append(f"The Pokemon needs to hold {name}")
                    elif k == "party_type_id":
                        l.append(
                            f"There has to be a {type_dict[v][0]} Pokemon in the party"
                        )
                    elif k == "party_species_id":
                        l.append(
                            f"A {id_dict[str(v)][1]} has to be present in the party"
                        )
            elif trig_id == 2:
                if not hmm.items():
                    l = ["Trade"]
                else:
                    l = ["Trade and"]
                for k, v in hmm.items():
                    if k == "held_item_id":
                        name = (item_id_dict[str(v)]).capitalize()
                        name = name.replace("-", " ")
                        l.append(f"The Pokemon needs to hold {name}")
                    elif k == "trade_species_id":
                        l.append(
                            f"A {id_dict[str(v)][1]} has to be present in the party"
                        )
            elif trig_id == 3:
                if not hmm.items():
                    l = ["Use item"]
                for k, v in hmm.items():
                    if k == "trigger_item_id":
                        name = (item_id_dict[str(v)]).capitalize()
                        name = name.replace("-", " ")
                        l.append(f"{name} needs to be used")
                    if k == "gender_id":
                        l.append(f"Gender has to be {'Male' if v==2 else 'Female'}")
            elif trig_id == 4:
                l.append(
                    "There needs to be a Poke Ball in the bag and \nthere also needs to be an empty slot in the party"
                )
            elif trig_id == 5:
                l.append(
                    "Select a sweet of your choice and give it to the Pokemon \n Then spin your in game avatar around."
                )
            elif trig_id == 6:
                l.append("Train in the Tower of Darkness")
            elif trig_id == 7:
                l.append("Train in the Tower of Waters")
            elif trig_id == 8:
                l.append("Land three critical hits in a battle")
            elif trig_id == 9:
                l.append("Go somewhere and take damage")
            if overworld_rain:
                l.append("It needs to be raining in the overworld")
            if upside_down:
                l.append("You need to flip the console upside-down")
            embed.add_field(name=f"{evolves_from} ➔ {evolves_to}", value="\n".join(l))
        embed = await add_info_to_embed(ctx, embed)
        if private is None:
            private = False
        return await ctx.send(embed=embed, ephemeral=private)

    @evolution.autocomplete("pokemon")
    @pokemon_autocomplete
    async def auto_evo_pokemon(self, interaction, current: str):
        ...

    @commands.command(
        name="compstats",
        aliases=["comp_stat", "stats_diff", "cstats", "compstat"]
    )
    async def compare_stats(self, ctx: commands.Context, *pokemon: str):
        """Compare the stats of 2 or more Pokemon. Limited to 10 Pokemon only."""
        embed = discord.Embed(title="Stats comparison")
        not_found = []
        new_list = []
        for poke in pokemon:
            pok = await PokedexConverter.convert(ctx=ctx, argument=poke)
            new_list.append(pok)
        new_list = list(set(new_list))
        if len(new_list) == 1 or len(new_list) > 10:
            return await ctx.send(
                "Please provide more than two Pokemon names and a maximum of 10"
            )
        for pok in new_list:
            stats = []
            total = 0
            stats_dict = pokedex_dict[pok]["baseStats"]
            for stat_name, value in stats_dict.items():
                stats.append(f"**{stat_name}**: {value}")
                total = total + value
            stats.append(f"**Total**: {total}")
            stats = ", ".join(stats)
            embed.add_field(
                name=pok.replace("-", " ").capitalize(), value=stats, inline=False
            )
        if x := len(not_found):
            if x == 1:
                embed.add_field(
                    name="Could not find a close match for this Pokemon :",
                    value=", ".join(not_found),
                )
            else:
                embed.add_field(
                    name="Could not find a close match for these Pokemon name(s) :",
                    value=", ".join(not_found),
                )

        embed = await add_info_to_embed(ctx, embed)
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        f"{Pokemon.__qualname__} up"

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # if message.content.split()[2].lower()=="sprite":return
        if not getattr(self, "SpriteConverter", False):
            self.SpriteConverter = SpriteConverter()  # type:ignore
        if message.author.bot:
            return
        if message.guild is None:
            strings = list(
                set(
                    [
                        i.groupdict()["name"]
                        for i in SPRITE_REGEX.finditer(message.content)
                    ]
                )
            )[:4]
            if not strings:
                return
            else:
                ctx: commands.Context = await self.bot.get_context(message)
                if ctx.command is not None:
                    return
            for content in strings:
                try:
                    await ctx.invoke(
                        self.sprite,
                        sprite_name=await self.SpriteConverter.convert(ctx, content),
                    )
                except commands.BadArgument:
                    pass
        elif message.guild.id != 336642139381301249:
            strings = list(
                set(
                    [
                        i.groupdict()["name"]
                        for i in SPRITE_REGEX.finditer(message.content)
                    ]
                )
            )[:4]
            if not strings:
                return
            else:
                ctx: commands.Context = await self.bot.get_context(message)
                if ctx.command is not None:
                    return
            for content in strings:
                try:
                    ctx: commands.Context = await self.bot.get_context(message)
                    await ctx.invoke(
                        self.sprite,
                        sprite_name=await self.SpriteConverter.convert(ctx, content),
                    )
                except:
                    pass

    def cog_load(self) -> None:
        if (moveset_command := self.bot.get_command("moveset")) is not None:
            setattr(moveset_command, "helpcog", self)
        if not hasattr(self, "extracommands") or not self.extracommands and moveset_command is not None:
            self.extracommands = [moveset_command]


async def setup(bot):
    await bot.add_cog(Pokemon(bot))
