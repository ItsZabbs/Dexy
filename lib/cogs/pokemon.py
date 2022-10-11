import gc
import json
import discord
from typing import Dict,List, Optional
from discord.ext import commands,tasks
from discord.ext.commands import parameter
from discord import app_commands
import difflib
import random
from typing import Tuple
from copy import deepcopy

import aiohttp
import re

from lib.bot import Bot

from ..db import db
type_emoji_dict = {'bug': '<:bug:985953221409394759>', 'dark': '<:dark:985953337256071199>', 'dragon': '<:dragon:985953408575995914>', 'electric': '<:electric:985953515681767465>', 'fairy': '<:fairy:985953654093795338>', 'fighting': '<:fighting:985953721735323678>', 'fire': '<:fire:985955119755567125>', 'flying': '<:flying:985955123303948358>', 'ghost': '<:ghost:985955415315595284>',
                   'grass': '<:grass:985955439734841394>', 'ground': '<:ground:985955963309813781>', 'ice': '<:ice:985955967600574525>', 'normal': '<:normal:985955971094417478>', 'poison': '<:poison:985955973178986537>', 'psychic': '<:psychic:985956204993978439>', 'rock': '<:rock:985956212388548668>', 'steel': '<:steel:985956509156515920>', 'water': '<:water:985956512679735328>'}
version_names = ['Red, Blue', 'Yellow', 'Gold, Silver', 'Crystal', 'Ruby, Sapphire', 'Emerald', 'Firered, Leafgreen', 'Diamond, Pearl', 'Platinum', 'Heartgold, Soulsilver', 'Black, White', 'Colosseum',
                 'Xd', 'Black 2, White 2', 'X, Y', 'Omega Ruby, Alpha Sapphire', 'Sun, Moon', 'Ultra Sun, Ultra Moon', 'Lets Go Pikachu, Lets Go Eevee', 'Sword, Shield', 'Brilliant Diamond, Shining Pearl','Legends Arceus']
serebii="https://www.serebii.net/pokemon/art/"
back_dict = {'afd': 'afd-back', 'none': 'ani-back', 'gen1': 'gen1-back', 'rgb': 'gen1rgb-back', 'gen2': 'gen2-back',
            'gen3': 'gen3-back', 'rb': 'gen3-back', 'pt': 'gen4-back', 'bw': 'gen5-back', 'bwani': 'gen5ani-back'}
normal_dict = {'bw': 'gen5', 'bwani': 'gen5ani', 'none': 'ani', 'afd': 'afd', 'hgss':'gen4','pt': 'gen4dp-2', 'dp': 'gen4dp',
            'gen3': 'gen3', 'rs': 'gen3rs', 'frlg': 'gen3frlg', 'gold': 'gen2g', 'silver': 'gen2s',
            'crystal': 'gen2', 'rb': 'gen1rb', 'rg': 'gen1rg', 'yellow': 'gen1', 'gen1': 'gen1','gen5':'gen5','gen4':'gen4'}
version_dict={'red-blue': '1', 'yellow': '2', 'gold-silver': '3', 'crystal': '4', 'ruby-sapphire': '5', 'emerald': '6', 'firered-leafgreen': '7', 'diamond-pearl': '8', 'platinum': '9', 'heartgold-soulsilver': '10', 'black-white': '11', 'colosseum': '12', 'xd': '13', 'black 2-white 2': '14', 'x-y': '15', 'omega ruby-alpha sapphire': '16', 'sun-moon': '17', 'ultra sun-ultra moon': '18', 'lets go pikachu-lets go eevee': '19', 'sword-shield': '20','brilliant diamond-shining pearl':'21'}
initial_dict={'rb': '1', 'y': '2', 'gs': '3', 'c': '4', 'rs': '5', 'e': '6', 'frlg': '7', 'dp': '8', 'pt': '9', 'hgss': '10', 'bw': '11', 'co': '12', 'xd': '13', 'b2w2': '14', 'xy': '15', 'oras': '16', 'sm': '17', 'usum': '18', 'lgp': '19','lge': '19', 'swsh': '20','bdsp':'21','pla':'99'}
learn_list={'level-up': {'id': 1}, 'egg': {'id': 2}, 'tutor': {'id': 3}, 'tm': {'id': 4},'technical machine':{'id':4}, 'stadium-surfing-pikachu': {'id': 5}, 'light-ball-egg': {'id': 6}, 'colosseum-purification': {'id': 7}, 'xd-shadow': {'id': 8}, 'xd-purification': {'id': 9}, 'form-change': {'id': 10}, 'zygarde-cube': {'id': 11}}
type_dict = {1: ('Normal', (168, 168, 120)), 2: ('Fighting', (192, 48, 40)), 3: ('Flying', (168, 144, 240)),
            4: ('Poison', (160, 64, 160)), 5: ('Ground', (224, 192, 104)), 6: ('Rock', (184, 160, 56)),
            7: ('Bug', (168, 184, 32)), 8: ('Ghost', (112, 88, 152)), 9: ('Steel', (184, 184, 208)),
            10: ('Fire', (240, 128, 48)),
            11: ('Water', (104, 144, 240)), 12: ('Grass', (120, 200, 80)), 13: ('Electric', (248, 208, 48)),
            14: ('Psychic', (248, 88, 136)), 15: ('Ice', (152, 216, 216)), 16: ('Dragon', (112, 56, 248)),
            17: ('Dark', (112, 88, 72)), 18: ('Fairy', (238, 153, 172)), 10001: ('Unknown', (104, 160, 144)),
            10002: ('Shadow', (104, 160, 144))}
colour_dict={'normal': (168, 168, 120), 'fighting': (192, 48, 40), 'flying': (168, 144, 240), 'poison': (160, 64, 160), 'ground': (224, 192, 104), 'rock': (184, 160, 56), 'bug': (168, 184, 32), 'ghost': (112, 88, 152), 'steel': (184, 184, 208), 'fire': (240, 128, 48), 'water': (104, 144, 240), 'grass': (120, 200, 80), 'electric': (248, 208, 48), 'psychic': (248, 88, 136), 'ice': (152, 216, 216), 'dragon': (112, 56, 248), 'dark': (112, 88, 72), 'fairy': (238, 153, 172), 'unknown': (104, 160, 144), 'shadow': (104, 160, 144)}
BaseURL = "https://play.pokemonshowdown.com/sprites/"

#Alias cache implementation
alias_cache:Dict[List,List]={}
pokemon_names:list=json.load(open("lib/cogs/pokedexdata/pokemon_names.json"))
pokemon_names_ani:list=json.load(open("lib/cogs/pokedexdata/pokemon_names_ani.json"))
location_dict=json.load(open("lib/cogs/pokedexdata/location_dict.json",encoding='utf-8'))
evol_lines=json.load(open("lib/cogs/pokedexdata/pokemon_evolution_lines.json",encoding='utf-8'))
damage_dict = {1: '<:status:855828384139051048>',
            2: '<:physical:855828733880303626>', 3: '<:special:855828580533796864>'}
target_dict = {1: 'Specific Move',
            2: 'Selected Pokemon or Me First',
            3: 'Ally',
            4: 'Users side',
            5: 'User or Ally',
            6: 'Opponents Side',
            7: 'User',
            8: 'Random Opponent',
            9: 'All other Pokemon',
            10: 'Selected Pokemon',
            11: 'All Opponents',
            12: 'Entire Side',
            13: 'User and Allies',
            14: 'All Pokemon'}
abil_rating_dict = {-3:'Absolute Trash',-2:'Harmful',-1: 'Detrimental', 0: 'Useless', 1: 'Ineffective',
                    2: 'Useful', 3: 'Effective', 4: 'Very Useful', 5: 'Essential'}
with open("lib/cogs/pokedexdata/typechart.json", encoding='utf-8') as typechart:
    types: dict = json.load(typechart)
with open("lib/cogs/pokedexdata/pokemon_stuff_english_only.json", encoding='utf-8') as hmm:
    pokedex_dict: dict = json.load(hmm)
    id_dict={}
    for k,v in pokedex_dict.items():
        if id_dict.get(str(v["num"]),None) is None:
            id_dict[str(v["num"])]=(k,v["name"])
    pokemon_names_disp=[v["name"] for v in pokedex_dict.values()]
with open("lib/cogs/pokedexdata/nonexistentfile.json", encoding='utf-8') as pee:
    moves_dict: dict = json.load(pee)
    moveid_dict={}
    for k,v in moves_dict.items():
        ide=v["id"]
        moveid_dict[ide]=k
    move_names=tuple(moves_dict.keys())
evol_dict=json.load(open("lib/cogs/pokedexdata/pokemon_evolutions.json",encoding='utf-8'))
with open('lib/cogs/pokedexdata/abilities_flavour_text_english_only.json', encoding='utf-8') as abilflav:
    abil_flav_dict: dict = json.load(abilflav)
with open('lib/cogs/pokedexdata/ability_stuff.json', encoding='utf-8') as abilstuff:
    abil_stuff_dict: dict = json.load(abilstuff)
    abil_names=tuple(v["name"] for v in abil_stuff_dict.values())
with open('lib/cogs/pokedexdata/item_names_and_flavour_combined_english.json',encoding='utf-8') as item_st:
    item_stuff_dict: dict = json.load(item_st)
item_id_dict=json.load(open("lib/cogs/pokedexdata/item_names_english_only.json",encoding='utf-8'))
item_names=tuple(name for name in item_id_dict.values())
with open("lib/cogs/pokedexdata/movesets.json",encoding='utf-8') as move:
    movesets=json.load(move)

messages=['Help in keeping the bot up! [Donate](https://buymeacoffee.com/Zabbs "buy me a coffee!!")','Donate for the server costs! [Donate](https://buymeacoffee.com/Zabbs "buy me a coffee!!")','Show your appreciation for the bot! [Donate here!](https://buymeacoffee.com/Zabbs "buy me a coffee!!")']
async def embed_this_please(embed:discord.Embed):
    if random.randint(1,30)==1:
        embed.add_field(name="It also seems that you're enjoying the bot...",value=f'Care to write a review on [top.gg](https://top.gg/bot/853556227610116116)?\n {random.choice(messages)}')
    embed.set_footer(text="The bot has undergone some changes. PLEASE read it's about me for more info. \n\
        You can also join the support server to be informed of any updates and downtimes.")
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

        types = " , ".join(pokemon_dict["types"])
        if len(pokemon_dict["types"]) == 1:
            multipleTypes = "Type"
        else:
            multipleTypes = "Types"
        name = " ".join(n.capitalize() for n in pokemon_dict["name"].replace("-"," ").split())
        # name:str=name.replace("-"," ")
        # name=" ".join(n.capitalize() for n in name.split())
        colour: list = pokemon_dict["color"]
        if not isinstance(colour,list):
            colour=(88, 101, 242)
        # Title is the name
        try:
            dex_entry = random.choice(pokemon_dict["flavourText"])
        except KeyError:
            try:  # Temporary fix to the swsh pokemon not having dex entries
                dex_entry = random.choice(
                    pokedex_dict[pokemon_dict["baseSpecies"].lower()]["flavourText"])
            except:
                dex_entry = ""
        if dex_entry != "":
            embed = discord.Embed(
                title=name, description=f"*{dex_entry}*", colour=discord.Color.from_rgb(*colour))
        # then the next field is the types
        else:
            embed = discord.Embed(
                title=name, colour=discord.Color.from_rgb(*colour))
        embed.add_field(name=f"{multipleTypes}", value=f'{types}', inline=True)

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
                genderRatio="No Gender" if genderRatio=="N" else "Male" if genderRatio=="M" else "Female"
            except KeyError:
                genderRatio = "50% for both genders"
        if genderRatio != "":
            # third field is gender
            embed.add_field(name="**Gender Percentage**",
                            value=f"{genderRatio}", inline=True)
        embed.add_field(name='**Stats**', value=f"{stats}", inline=False)

        # The entire evolution check depends on the fact that there are no 4 chain evolutions
        try:
            # Try checking if the first evolution exists. For example , Psyduck to Golduck
            firstevo = pokemon_dict["evos"]
            EvoString = "**" + name.capitalize() + "**" + " → " + firstevo[0]
            try:
                secondevo = (pokedex_dict[f"{firstevo[0].lower()}"])["evos"]
                EvoString = "**" + name.capitalize() + "**" + " → " + \
                            firstevo[0] + " → " + secondevo[0]
            except KeyError:
                try:
                    pre_evo = pokemon_dict["prevo"]
                    EvoString = pre_evo + " → " + "**" + name.capitalize() + "**" + \
                        " → " + firstevo[0]
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
                    pre_evo_of_pre_evo = (
                        pokedex_dict[f"{pre_evo.lower()}"])["prevo"]
                    EvoString = pre_evo_of_pre_evo + " → " + pre_evo + \
                        " → " + "**" + name.capitalize() + "**"
                except:
                    # The pokemon is lonely like dunsparce with no evolutions before or after.
                    pass
            except:
                EvoString = ""
                pass
        if EvoString != "":
            embed.add_field(name="**Evolution**",
                            value=f"{EvoString}", inline=False)

        try:
            url = pokemon_dict["url"]
        except KeyError:
            url = ""
        if len(pokemon_dict["eggGroups"]) == 1:
            Egg = "Egg Group"
        else:
            Egg = "Egg Groups"
        if url != "":
            embed.set_thumbnail(url=serebii+url+".png")
            #embed.set_footer(text="Please report any wrong artwork/icons using the `feedback` command!")
        embed.insert_field_at(
            2, name=f"**{Abilities}**", value=f"{abilities}", inline=True)
        height = pokemon_dict["heightm"]
        weight = pokemon_dict["weightkg"]
        tier = pokemon_dict['Tier']
        urllist = []
        try:
            name = pokemon_dict['baseSpecies']
        except KeyError:
            pass
        if pokemon_dict['num'] <= 0:
            name = (name.replace(" ", "-")).lower()
            urllist.append(
                f"[Smogon](https://www.smogon.com/dex/ss/pokemon/{name})")
        else:
            name = name.replace(" ", "_")
            urllist.append(
                f"[Bulbapedia](https://bulbapedia.bulbagarden.net/wiki/{name})")
            name = (name.replace(" ", "-")).lower()
            urllist.append(
                f"[PokemonDB](https://pokemondb.net/pokedex/{name})")
            urllist.append(
                f"[Smogon](https://www.smogon.com/dex/ss/pokemon/{name}/)")
            urllist.append(
                f"[Serebii](https://www.serebii.net/pokemon/{name})")
        embed.add_field(name="**Height**", value=f"{height} m", inline=False)
        embed.add_field(name="**Weight**", value=f"{weight} kg", inline=True)
        embed.add_field(name="**Smogon Tier**", value=f"{tier}", inline=True)
        embed.add_field(
            name=f"**{Egg}**", value=f"{', '.join(pokemon_dict['eggGroups'])}", inline=False)
        embed.add_field(name='**External Resources**',
                        value=f"{' • '.join(urllist)}", inline=False)
        return embed
    else:
        embed = discord.Embed(
            title=" ".join(n.capitalize() for n in pokemon_dict["name"].replace("-"," ").split()), colour=discord.Color.from_rgb(*pokemon_dict["color"]))
        types = " , ".join(pokemon_dict["types"])
        if len(pokemon_dict["types"]) == 1:
            multipleTypes = "Type"
        else:
            multipleTypes = "Types"
        try:
            embed.set_thumbnail(url=serebii+pokemon_dict['url']+".png")
            #embed.set_footer(text="Please report any wrong artwork/icons using the `feedback` command!")
        except:
            pass
        embed.add_field(name='**Types**', value=f'{types}', inline=False)
        embed.add_field(name='**Abilities**',
                        value=f'{abilities}', inline=True)
        embed.add_field(name='**Stats**', value=f'{stats}', inline=False)
        return embed


async def convert_move_to_embed(name, move_provided, flavourmmm):
    power: int = move_provided['power']
    accuracy: str = str(move_provided['accuracy'])
    if accuracy != "None":
        accuracy += "%"
    pp: int = move_provided['pp']
    title: str = damage_dict[move_provided['damage_class_id']] + " " + name
    if isinstance((n:=move_provided['generation_id']),int):
        flavourmmm=flavourmmm+f'\n*Generation introduced: {n}*'
    embed = discord.Embed(title=title, description=flavourmmm, colour=discord.Color.from_rgb(
        *(type_dict[move_provided['type_id']])[1]))
    embed.add_field(
        name='Type', value=f"{type_dict[move_provided['type_id']][0]}", inline=True)
    embed.add_field(name='PP', value=f'{pp}', inline=True)
    embed.add_field(name='Base Power', value=f'{power}', inline=True)
    embed.add_field(name='Accuracy', value=f"{accuracy}", inline=True)
    embed.add_field(
        name='Target', value=f"{target_dict[move_provided['target_id']]}", inline=True)
    embed.add_field(name='Priority',
                    value=f"{move_provided['priority']}", inline=True)
    return embed


async def convert_four_baseurl(back: bool, shiny: bool, pokemon: str, sprite_type: str, ctx: commands.Context):
    if back:
        try:
            url = back_dict[sprite_type]
            if shiny and 'gen2g' not in url and 'gen1' not in url and 'gen2s' not in url:
                url = url + "-shiny"
            url = url + "/" + pokemon + (".gif" if "ani" in url else ".png")
        except KeyError:
            raise KeyError(
                "That sprite type was not found for back sprites...")
    else:
        try:
            url = normal_dict[sprite_type]
            if shiny and 'gen2g' not in url and 'gen1' not in url and 'gen2s' not in url:
                url = url + "-shiny"
            url = url + "/" + pokemon + (".gif" if "ani" in url else ".png")
        except KeyError:
            raise KeyError(
                f"Couldn't find that sprite type... Try seeing {ctx.prefix}help sprite for all the available sprite types...")
    return url


async def convert_string_sprite_to_structured(x, ctx:commands.Context) -> Tuple[str,str,str,str]:
    x=x.replace("-"," ")
    lis = ('rs', 'bw', 'yellow', 'gen3', 'gen1', 'rb', 'gen5', 'silver', 'pt', 'rg',
        'frlg', 'dp', 'gold', 'bwani', 'gen2', 'gen5ani', 'crystal', 'gen4',
        'afd', 'gen2g', 'gen2s','hgss','dp','pt','gen4')
    x = x.lower()
    try:
        if ctx.guild.id in alias_cache:
            existingaliases,existingsprites=alias_cache[ctx.guild.id]
        else:
            existingaliases:List = (db.field("SELECT Aliases from guilds WHERE GuildID = ?", ctx.guild.id)).split(";")
            existingsprites:List = (db.field("SELECT AliSprites from guilds WHERE GuildID = ?", ctx.guild.id)).split("|")
            if len(alias_cache)>120:
                alias_cache.pop(tuple(alias_cache.keys())[0])
            alias_cache[ctx.guild.id]=existingaliases,existingsprites
        #return commands.when_mentioned_or(*prefix_cache[message.guild.id])(user, message)
        # existingaliases = (db.field(
        #     "SELECT Aliases from guilds WHERE GuildID = ?", ctx.guild.id)).split(";")
        # existingsprites = (db.field(
        #     "SELECT AliSprites from guilds WHERE GuildID = ?", ctx.guild.id)).split("|")
        if x in existingaliases:
            x = existingsprites[existingaliases.index(x)]
    except:
        pass
        # raise NameError("Could not find that pokemon")
    x = "  ".join(x.split())
    back = False
    if re.search("back", x):
        x = re.sub("back", "", x)
        back = True
    shiny = False
    if re.search("shiny", x):
        x = re.sub("shiny", "", x)
        shiny = True
    x = " " + x + " "
    result = re.findall(" | ".join(lis), x)
    while "" in result:
        result.remove("")
    if not result:
        result = ""
    else:
        result = result[0]
    x = re.sub(result, "", x).strip()
    x = re.sub("gigantamax", "gmax", x)
    x = re.sub("mega y", "megay", x)
    x = re.sub("mega x", "megax", x)
    x = re.sub("female", "f", x)
    x = re.sub("galarian", "galar", x)
    x = re.sub("alolan", "alola", x)
    x = re.sub("hisuian","hisui",x)
    x = x.split()
    if x[0].startswith("tapu") and len(x)>1:
        x=x[0]+x[1]
    elif len(x) > 1:
        x = x[0] + "-" + "-".join(x[1:])
    else:
        x = x[0]
    x=x.lower()
    if x=="meganium":
        pass
    elif x.startswith((
            "crowned", "origin", "dusk-mane", 'duskmane', 'dawnwings', 'dawn-wings', "megax", "megay", "female",
            "galar", "alola", "mega", "gmax", "eternamax","hisui")):
        x = x.split("-")
        x = x[-1] + "-" + ("".join((x[-2::-1])[::-1]))
    result = result if result else "None"
    resultsprite:str = result.strip().lower()
    pokemon_name:str=x
    back:str=back
    shiny:str=shiny
    return back, shiny, resultsprite,pokemon_name,


class Pokemon(commands.Cog):
    '''All of the Pokemon related commands'''
    url="pokemon-related-commands"
    def __init__(self, bot:Bot):
        self.bot = bot
        self.bot.alias_cache=alias_cache
        self.cleanup_gc.start()
    def cog_unload(self):
        self.cleanup_gc.stop()
    @commands.group(extras={'url':"alias-management"})
    async def alias(self, ctx: commands.Context):
        '''Alias commands for sprites'''
        if ctx.invoked_subcommand is None:
            pass

    @alias.command(name='add',extras={"url":"span-stylecoloryellowhow-to-add-an-alias-span"})
    @commands.has_permissions(manage_guild=True)
    async def add_alias(self, ctx: commands.Context, alias: str=parameter(description="The text that will call the sprite."), *, sprite: str=parameter(description="The sprite that will be called via the alias.")):
        '''Adds an alias to a sprite for easy access and memes'''
        sprite = sprite.lower()
        alias = alias.lower()
        back, shiny, sprite_type, pokemon = await convert_string_sprite_to_structured(sprite, ctx)
        if ";" in alias:
            return await ctx.send("Alias cannot contain a semicolon!")
        url = await convert_four_baseurl(back, shiny, pokemon, sprite_type.lower(), ctx)
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url=BaseURL + url) as r:
                if r.status != 200:
                    name = difflib.get_close_matches(pokemon, pokedex_dict.keys(),n=1)
                    if not name:
                        raise KeyError(
                            "Looks like the pokemon you requested doesn't exist...")
                    name=name[0]
                    pokemon_dict = pokedex_dict[name]
                    if name == pokemon_dict["name"].lower():
                        raise KeyError(
                            "The sprite is not available in that format...")
                    *_,name=await convert_string_sprite_to_structured(name,ctx)
                    raise KeyError(
                        f"Were you looking for {name}?")
        if ctx.guild.id in self.bot.alias_cache:
            existingaliases,existingsprites=self.bot.alias_cache[ctx.guild.id]
        else:
            try:
                existingaliases = (db.field(
                    "SELECT Aliases from guilds WHERE GuildID = ?", ctx.guild.id)).split(";")
                existingsprites = (db.field(
                    "SELECT AliSprites from guilds WHERE GuildID = ?", ctx.guild.id)).split("|")
            except:
                existingaliases = []
                existingsprites = []
            if len(self.bot.alias_cache)>120:
                self.bot.alias_cache.pop(tuple(self.bot.alias_cache.keys())[0])
            self.bot.alias_cache[ctx.guild.id]=existingaliases,existingsprites
        if alias in existingaliases:
            return await ctx.send("That's an existing alias!")
        existingsprites.append(sprite)
        existingaliases.append(alias)
        self.bot.alias_cache.update({ctx.guild.id:(existingaliases,existingsprites)})
        existingaliases = ";".join(existingaliases)
        existingsprites = "|".join(existingsprites)
        db.execute(
            f"UPDATE guilds SET Aliases=? WHERE GuildID = {ctx.guild.id}", existingaliases)
        db.execute(
            f"UPDATE guilds SET AliSprites=? WHERE GuildID = {ctx.guild.id}", existingsprites)
        await ctx.message.add_reaction("<:greenTick:596576670815879169>")

    @alias.command(name='remove',extras={"url":"span-stylecoloryellowhow-to-remove-an-alias-span"})
    @commands.has_permissions(manage_guild=True)
    async def remove_alias(self, ctx, alias:str=parameter(description="The alias to remove.")):
        '''Removes an existing alias'''
        if ctx.guild.id in self.bot.alias_cache:
            existingaliases,existingsprites=self.bot.alias_cache[ctx.guild.id]
        else:
            try:
                existingaliases = (db.field(
                    "SELECT Aliases from guilds WHERE GuildID = ?", ctx.guild.id)).split(";")
                existingsprites = (db.field(
                    "SELECT AliSprites from guilds WHERE GuildID = ?", ctx.guild.id)).split("|")
            except:
                return await ctx.send("You do not have any aliases set for this server!")
            if len(self.bot.alias_cache)>120:
                self.bot.alias_cache.pop(tuple(self.bot.alias_cache.keys())[0])
            self.bot.alias_cache[ctx.guild.id]=existingaliases,existingsprites
        # try:
        #     existingaliases = (db.field(
        #         "SELECT Aliases from guilds WHERE GuildID = ?", ctx.guild.id)).split(";")
        #     existingsprites = (db.field(
        #         "SELECT AliSprites from guilds WHERE GuildID = ?", ctx.guild.id)).split("|")
        # except:
        #     return await ctx.send("You do not have any aliases set for this server!")
        try:
            index = existingaliases.index(alias)
            existingaliases.pop(index)
            existingsprites.pop(index)
        except:
            return await ctx.send("There's no alias like that!")
        self.bot.alias_cache.update({ctx.guild.id:(existingaliases,existingsprites)})
        existingaliases = ";".join(existingaliases)
        existingsprites = "|".join(existingsprites)
        db.execute(
            f"UPDATE guilds SET Aliases=? WHERE GuildID = {ctx.guild.id}", existingaliases)
        db.execute(
            f"UPDATE guilds SET AliSprites=? WHERE GuildID = {ctx.guild.id}", existingsprites)
        await ctx.message.add_reaction("<:greenTick:596576670815879169>")

    @alias.command(name='list',extras={"url":"span-stylecoloryellowhow-to-list-all-aliases-span"})
    async def list_aliases(self, ctx):
        '''Lists all the server aliases for a pokemon'''
        if ctx.guild.id in self.bot.alias_cache:
            existingaliases,existingsprites=self.bot.alias_cache[ctx.guild.id]
        else:
            try:
                existingaliases = (db.field(
                    "SELECT Aliases from guilds WHERE GuildID = ?", ctx.guild.id)).split(";")
                existingsprites = (db.field(
                    "SELECT AliSprites from guilds WHERE GuildID = ?", ctx.guild.id)).split("|")
            except:
                return await ctx.send("You do not have any aliases set for this server!") 
            if len(self.bot.alias_cache)>120:
                self.bot.alias_cache.pop(tuple(self.bot.alias_cache.keys())[0])
            self.bot.alias_cache[ctx.guild.id]=existingaliases,existingsprites
        # try:
        #     existingaliases = (db.field(
        #         "SELECT Aliases from guilds WHERE GuildID = ?", ctx.guild.id)).split(";")
        #     existingsprites = (db.field(
        #         "SELECT AliSprites from guilds WHERE GuildID = ?", ctx.guild.id)).split("|")
        # except:
        #     return await ctx.send("You do not have any aliases set for this server!")
        aliases=[]
        for n,(e,v) in enumerate(zip(existingaliases,existingsprites),start=1):
            if e or v:
                aliases.append(f'{n} : `{e}` ➔ `{v}`')
        if not aliases:
            return await ctx.send("You do not have any aliases set for this server!") 
        # aliases = [ for n, (e, v) in enumerate(
        #     zip(existingaliases, existingsprites) if (e or v), start=1)]
        
        embed = discord.Embed(title=f'Aliases for this server ({ctx.guild.name})', description="\n".join(aliases),
                            colour=discord.Color.blurple())

        await ctx.send(embed=embed)

    @commands.hybrid_command(name='ability', aliases=['abil'],extras={"url":"abilities"})
    @app_commands.describe(ability="The ability you want to get information on",private="If only you want to see the info.")
    async def ability(self, ctx: commands.Context, *, ability: str=parameter(description="The ability name to see info on"),private:Optional[bool]=parameter(description="If only you want to see the info. (Only slash commands)",default=False)):
        '''Sends information about the ability'''
        ability = ability.lower()
        ability = ability.replace(" ", "")
        try:
            abil_dict = abil_stuff_dict[ability]
        except KeyError:
            try:
                name =difflib.get_close_matches(ability, abil_stuff_dict.keys(),n=1)
                if not len(name):
                    raise NameError("Could not find that Ability.")
                name=name[0]
                if not name:
                    return await ctx.send("Looks like the ability you requested doesn't exist...")
                abil_dict = abil_stuff_dict[name]
            except KeyError:
                return await ctx.send("You've sent an incorrect spelling or a wrong ability name")
        name = abil_dict['name']
        urldict = []
        realname = name.replace(" ", "_")
        urldict.append(f"[Bulbapedia](https://bulbapedia.bulbagarden.net/wiki/{realname}_(Ability%29)")
        underscorename = name.replace(" ", "-")
        urldict.append(
            f"[PokemonDB](https://pokemondb.net/ability/{underscorename})")
        urldict.append(
            f"[Smogon](https://www.smogon.com/dex/ss/abilities/{underscorename}/)")
        nospacesname = (name.replace(" ", "")).lower()
        urldict.append(
            f"[Serebii](https://www.serebii.net/abilitydex/{nospacesname}.shtml)")
        embed = discord.Embed(title=f'{abil_dict["name"]}', description="No flavour text" if abil_flav_dict.get(str(abil_dict['num']),"No flavour text")=="No flavour text" else abil_flav_dict.get(str(abil_dict['num']))[-1] , colour=discord.Color.blurple())
        embed.add_field(name='Smogon Rating',
                        value=f"{abil_rating_dict[int(abil_dict['rating'])]} ({abil_dict['rating']})", inline=True)
        embed.add_field(name='External Resources',
                        value=f'{" • ".join(urldict)}', inline=False)
        embed=await embed_this_please(embed)
        await ctx.send(embed=embed,ephemeral=private)

    @ability.autocomplete('ability')
    async def abil_auto(self,interaction:discord.Interaction,current:str):
        return [
        app_commands.Choice(name=ability, value=ability)
        for ability in abil_names if current.lower() in ability.lower()
    ][:25]
    @commands.command(name='type',aliases=['weak'],extras={"url":"type-matchup-calculations"})
    async def type(self, ctx: commands.Context, *, pokemon_or_move_or_typestring: str=parameter(description="The Pokemon name or the move name or the type(s) to see the matchup on")):
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
        image_link=""
        name=""
        try:
            [types[e]["damageTaken"] for e in pokemon_or_move_or_typestring.split()]
            if len(pokemon_or_move_or_typestring.split())>2:
                return await ctx.send("You can't send more than two types.")
        except KeyError:
            try:
                name = difflib.get_close_matches(pokemon_or_move_or_typestring, pokedex_dict.keys(), n=1,cutoff=0.9)
                pokemon_or_move_or_typestring = " ".join(pokedex_dict[name[0]]["types"]).lower()
                image_link=pokedex_dict[name[0]].get("url","")
                if image_link:
                    image_link=f"https://www.serebii.net/pokemon/art/{image_link}.png"
            except:
                try:
                    name = difflib.get_close_matches(pokemon_or_move_or_typestring, moves_dict.keys(), n=1)
                    pokemon_or_move_or_typestring = type_dict[moves_dict[name[0]]["type_id"]][0].lower()
                except:
                    return await ctx.send("I couldn't match your input to a type or pokemon or move")

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
            for k, v in types.items():
                v = v["damageTaken"]
                if v[two.capitalize()] == 1:
                    supereffectiveTo.append(k.capitalize())
                elif v[two.capitalize()] == 0:
                    effectiveTo.append(k.capitalize())
                elif v[two.capitalize()] == 2:
                    resistantTo.append(k.capitalize())
                else:
                    immuneTo.append(k.capitalize())
        if len(pokemon_or_move_or_typestring.split())>1:
            for e in immuneFrom:
                if e in supereffectiveFrom:
                    supereffectiveFrom.remove(e)
            neweffectiveFrom=effectiveFrom.copy()
            for e in neweffectiveFrom:
                if e in supereffectiveFrom:
                    effectiveFrom.remove(e)
                elif e in immuneFrom:
                    effectiveFrom.remove(e)
                elif e in resistantFrom:
                    effectiveFrom.remove(e)
            newresistantfrom=resistantFrom.copy()
            for e in newresistantfrom:
                if e in supereffectiveFrom:
                    effectiveFrom.append(e)
                    supereffectiveFrom.remove(e)
                    resistantFrom.remove(e)
            ## OFFENSE
            for e in immuneTo:
                if e in supereffectiveTo:
                    supereffectiveTo.remove(e)
            neweffectiveTo=effectiveTo.copy()
            for e in neweffectiveTo:
                if e in supereffectiveTo:
                    effectiveTo.remove(e)
                elif e in immuneTo:
                    effectiveTo.remove(e)
                elif e in resistantTo:
                    effectiveTo.remove(e)
            newresistantfrom=resistantTo.copy()
            for e in newresistantfrom:
                if e in supereffectiveTo:
                    effectiveTo.append(e)
                    supereffectiveTo.remove(e)
                    resistantTo.remove(e)
            
        if len(pokemon_or_move_or_typestring.split())>1:
            if len(set(supereffectiveFrom)) != len(supereffectiveFrom):
                repeatedTypes = [
                    x for x in supereffectiveFrom if supereffectiveFrom.count(x) > 1]
                for e in set(repeatedTypes):
                    supereffectiveFrom.remove(e)
                    ind = supereffectiveFrom.index(e)
                    supereffectiveFrom[ind] =f"**{supereffectiveFrom[ind]}**"
            if len(set(resistantTo)) != len(resistantTo):
                repeatedTypes = [x for x in resistantTo if resistantTo.count(x) > 1]
                for e in set(repeatedTypes):
                    resistantTo.remove(e)
                    ind = resistantTo.index(e)
                    resistantTo[ind] = "**"+resistantTo[ind]+"**"
            if len(set(supereffectiveTo)) != len(supereffectiveTo):
                repeatedTypes = [
                    x for x in supereffectiveTo if supereffectiveTo.count(x) > 1]
                for e in set(repeatedTypes):
                    supereffectiveTo.remove(e)
                    ind = supereffectiveTo.index(e)
                    supereffectiveTo[ind] = "**"+supereffectiveTo[ind]+"**"
            if len(set(resistantFrom)) != len(resistantFrom):
                repeatedTypes = [
                    x for x in resistantFrom if resistantFrom.count(x) > 1]
                for e in set(repeatedTypes):
                    resistantFrom.remove(e)
                    ind = resistantFrom.index(e)
                    resistantFrom[ind] = "**"+resistantFrom[ind]+"**"
        for ind, e in enumerate(resistantFrom, start=0):
            if not e.endswith("(x0.25)"):
                resistantFrom[ind] = e#+" (x0.5)"
        for ind, e in enumerate(supereffectiveTo, start=0):
                    if not e.endswith("(x4)"):
                        supereffectiveTo[ind] = e#+" (x2)"
        for ind, e in enumerate(resistantTo, start=0):
                    if not e.endswith("(x0.25)"):
                        resistantTo[ind] = e#+" (x0.5)"
        for ind, e in enumerate(supereffectiveFrom, start=0):
                    if not e.endswith("(x4)"):
                        supereffectiveFrom[ind] = e#+" (x2)"
        # embed.add_field(name='Defense\n\nWeak to',
        #                 value=", ".join(list(set(supereffectiveFrom))))
        # embed.add_field(name='Takes normal damage from',
        #                 value=", ".join(list(set(effectiveFrom))), inline=False)
        # embed.add_field(name='Takes half damage from',
        #                 value=", ".join(list(set(resistantFrom))), inline=False)
        # if immuneFrom:
        #     embed.add_field(name='Does not damage:',
        #                     value=", ".join(list(set(immuneFrom))), inline=False)
        # if len(typestring.split())==1:
        #     embed.add_field(name='\nAttack \n\nDoes Super Effective Damage to',
        #                     value=", ".join(list(set(supereffectiveTo))), inline=False)
        #     embed.add_field(name='Deals normal damage to',
        #                     value=", ".join(list(set(effectiveTo))), inline=False)
        #     embed.add_field(name='Deals half damage to',
        #                     value=", ".join(list(set(resistantTo))), inline=False)
        #     if immuneTo:
        #         embed.add_field(name='Does not take any damage from:',value=", ".join(list(set(immuneTo)).sort()), inline=False)
        # await ctx.send(embed=embed)
        if name:
            name=name[0].replace("-"," ")
            #name=[name] if type(name)==str else name
            name=name.split()
            name=" "+" ".join(n.capitalize() for n in name)
        else:name=""
        emojis=''.join([type_emoji_dict[e] for e in pokemon_or_move_or_typestring.split()])
        embed=discord.Embed(title=emojis+name,colour=discord.Color.from_rgb(*colour_dict[two]),description=', '.join([e.capitalize() for e in pokemon_or_move_or_typestring.split()]))
        embed.add_field(name='**__DEFENSE__**\n\n *Weak to:*',value=", ".join(dict.fromkeys(supereffectiveFrom)) if supereffectiveFrom else "None",inline=False)
        embed.add_field(name='*Takes normal damage from:* ',value=", ".join(dict.fromkeys(effectiveFrom)) if effectiveFrom else 'None',inline=False)
        embed.add_field(name='*Resists:*',value=", ".join(dict.fromkeys(resistantFrom)) if resistantFrom else 'None',inline=False)
        embed.add_field(name='*Is Immune from:*',value=", ".join(dict.fromkeys(immuneFrom))if immuneFrom else "None",inline=False)
        
        ##OFFENSIVE
        if len(pokemon_or_move_or_typestring.split())==1:
            embed.add_field(name='**__OFFENSE__**\n\n *Does super effective damage to:*',value=", ".join(dict.fromkeys(supereffectiveTo)) if supereffectiveTo else "None",inline=False)
            if effectiveTo:embed.add_field(name='*Deals normal damage to:* ',value=", ".join(dict.fromkeys(effectiveTo)) if effectiveTo else "None",inline=False)
            if resistantTo:embed.add_field(name='*Resisted by:*',value=", ".join(dict.fromkeys(resistantTo)) if resistantTo else "None",inline=False)
            if immuneTo:embed.add_field(name='*Does not affect:*',value=", ".join(dict.fromkeys(immuneTo)) if immuneTo else "None",inline=False)
        embed=await embed_this_please(embed)
        if image_link:
            embed.set_thumbnail(url=image_link)
        embed.set_footer(text='Bold indicates double weakness/resistance')
        await ctx.send(embed=embed)
    
    @commands.hybrid_command(name='item',extras={"url":"items"})
    @app_commands.describe(itemname="The item you want to get information on",private="If only you want to see the info.")
    async def iteminfo(self, ctx, *, itemname: str=parameter(description="The name of the item."),private:Optional[bool]=parameter(description="If only you want to see the info. (Only slash commands))",default=False)):
        '''Sends info about the item'''
        itemname = itemname.lower()
        itemname = itemname.replace(" ", "")
        try:
            flavour_text_item = item_stuff_dict[itemname]
        except KeyError:
            try:
                itemname = difflib.get_close_matches(itemname, item_stuff_dict.keys(),n=1)[0]
                item_dict = item_stuff_dict[itemname]
            except:
                return await ctx.send("You've sent an incorrect spelling or a wrong item name")
        flavour_text_item = item_dict["FlavourText"]
        sprite = item_dict['sprite']
        embed = discord.Embed(
            title=f'{itemname}', description=f'{flavour_text_item[-1]}', colour=discord.Color.blurple())
        if sprite:
            embed.set_thumbnail(url=sprite)
        underscorename = itemname.replace(" ", "_")
        hyphenlink = itemname.replace(" ", "-")
        urllist = []
        urllist.append(
            f"[Bulbapedia](https://bulbapedia.bulbagarden.net/wiki/{underscorename})")
        urllist.append(
            f"[PokemonDB](https://pokemondb.net/item/{hyphenlink.lower()})")
        urllist.append(
            f"[Smogon](https://www.smogon.com/dex/ss/items/{hyphenlink.lower()}/)")
        nospacelink = itemname.replace(" ", "")
        urllist.append(
            f"[Serebii](https://www.serebii.net/itemdex/{nospacelink.lower()}.shtml)")

        embed.add_field(name='External Resources',
                        value=f"{' • '.join(urllist)}", inline=False)
        embed=await embed_this_please(embed)
        await ctx.send(embed=embed,ephemeral=private)

    @iteminfo.autocomplete('itemname')
    async def auto_item(self,interaction:discord.Interaction,current:str):
        return [
        app_commands.Choice(name=item, value=item)
        for item in item_names if current.lower() in item.lower()
    ][:25]
    @commands.command(name='sprite', aliases=['sp'],extras={"url":"sprites"})
    async def sprite(self, ctx: commands.Context, *, sprite_name: str=parameter(description="The Pokemon you want to see the sprite of. Find a more detailed guide in the wiki.")):
        '''Sends the requested sprite. See [prefix]help sprite for more info.
        pokemon : Pokemon name
        sprite_type : Check the wiki for a detailed guide
        Note: gmax and mega can be done by <pokemon>-gmax and <pokemon>-mega\n'''
        sprite_name=sprite_name.lower()
        back, shiny, sprite_type, pokemon = await convert_string_sprite_to_structured(sprite_name, ctx)
        sprite_type = sprite_type.lower().strip()
        pokemon = pokemon.replace(" ", "").lower().strip()
        if pokemon.lower() == "dab":
            embed = discord.Embed()
            embed.set_image(
                url='https://cdn.discordapp.com/attachments/777782956357320714/868583991031234590/kadabra.png')
            return await ctx.send(embed=embed)
        try:
            if pokemon=="prandom" and sprite_type=="none":
                pokemon=random.choice(pokemon_names_ani)
            if pokemon == "prandom":
                pokemon = random.choice(pokemon_names)
            elif "-" not in pokemon:
                if pokemon not in pokemon_names:
                    raise KeyError
            else:
                pass
        except KeyError:
            name= difflib.get_close_matches(pokemon,pokemon_names,n=1,cutoff=0.8)
            if not len(name):
                raise NameError("Could not find that Pokemon")
            name=name[0]
            if not name:
                raise KeyError(
                    "Looks like the pokemon you requested doesn't exist...")
            raise KeyError(f"Were you looking for {name}?")
        if pokemon not in pokemon_names and not (pokemon in pokemon_names_ani and sprite_type=="none"):
            name=difflib.get_close_matches(pokemon,pokemon_names,n=1,cutoff=0.3)
            if not name:
                raise KeyError("Could not find that Pokemon")
            raise KeyError(f"Could not find that Pokemon, try `{name[0]}` instead")
        if pokemon in pokemon_names and pokemon not in pokemon_names_ani and sprite_type=="none":
            raise KeyError("Seems like the Pokemon only has a `bw` sprite.")
        url = await convert_four_baseurl(back, shiny, pokemon, sprite_type, ctx)
        # payload = "{}"
        # async with aiohttp.ClientSession() as cs:
        #     async with cs.get(url=BaseURL + url) as r:
        #         if r.status != 200:
        #             try:
        #                 pokemon_dict = pokedex_dict[name]
        #             except:
        #                 raise NameError(f"It seems that I couldn't find the sprite for {sprite_type} for {pokemon}. It seems that the sprite doesn't exist for the requested format.")
        #             name= difflib.get_close_matches(pokemon, pokedex_dict.keys())
        #             if not len(name):
        #                 raise NameError("Could not find that Pokemon.")
        #             name=name[0]
        #             if not name:
        #                 raise KeyError("Looks like the pokemon you requested doesn't exist...")
        #             # if name == pokemon_dict["name"].lower():
        #             #     raise KeyError("The sprite is not available in that format...")
        #             *_,name=await convert_string_sprite_to_structured(name,ctx)
        #             raise KeyError(
        #                 f"Were you looking for {name}?")
        
        embed = discord.Embed()
        embed.set_image(url=BaseURL+url)
        #embed=await embed_this_please(embed)
        return await ctx.send(embed=embed)
    
    # @app_commands.command(name='sprite',description='Sends the ingame sprite of the requested Pokemon',extras={"url":"sprites"})
    # async def sprite_slash(self,interaction:discord.Interaction,pokemon:str,version_name:Optional[str],back:Optional[bool]=False,shiny:Optional[bool]=False,private:Optional[bool]=False):
    #     await interaction.response.send_message("amogus sussy imposter",ephemeral=True)
    
    # @sprite_slash.autocomplete("pokemon")
    # async def sprite_autopokemon(self,interaction,current):
    #     return []
    @commands.hybrid_command(name='pokedex', aliases=['dex'],extras={"url":"pokedex"})
    @app_commands.describe(pokemon="The Pokemon you want to get information on",private="If only you want to see the info.",lite="If you want to get lightweight info.")
    async def pokedex(self, ctx:commands.Context, *, pokemon: str=parameter(description="The Pokemon you want to see the info on."),private:Optional[bool]=parameter(description="If only you want to see the info.",default=False),lite:Optional[bool]=False):
        '''Sends dex information about the pokemon'''
        try:
            existingaliases = (db.field("SELECT Aliases from guilds WHERE GuildID = ?", ctx.guild.id)).split(";")
            existingsprites = (db.field("SELECT AliSprites from guilds WHERE GuildID = ?", ctx.guild.id)).split("|")
            if pokemon in existingaliases:
                index = existingaliases.index(pokemon)
                pokemon = existingsprites[index]
        except AttributeError:
            pass
        pokemon = pokemon.lower()
        pokemon = pokemon.replace(" ", "")
        if pokemon=="random":
            pokemon=random.choice(pokemon_names)
        *_, pokemon = await convert_string_sprite_to_structured(pokemon, ctx)
        try:
            pokemon_dict = pokedex_dict[pokemon]
        except KeyError:
            try:
                name = difflib.get_close_matches(pokemon, pokedex_dict.keys(),n=1)[0]
                if not name:
                    return await ctx.send("Looks like the pokemon you requested doesn't exist...")
                pokemon_dict = pokedex_dict[name]
            except:
                return await ctx.send("You've sent an incorrect spelling or a wrong pokemon name")
        embed = await get_pokedex_stuff(pokemon_dict,lite)
        embed=await embed_this_please(embed)
        await ctx.send(embed=embed,ephemeral=private)

    @pokedex.autocomplete("pokemon")
    async def auto_dex(self,interaction,current:str):
        return [
        app_commands.Choice(name=pokemon, value=pokemon)
        for pokemon in pokemon_names_disp if current.lower() in pokemon.lower()
    ][:25]
    @commands.hybrid_command(name='ldex', aliases=['litedex', 'cheapdex'],extras={"url":"lite-pokedex"})
    @app_commands.describe(pokemon="The Pokemon you want to get information on",private="If only you want to see the info.")
    async def lite_dex(self, ctx, *, pokemon: str=parameter(description="The Pokemon you want to see the info on."),private:Optional[bool]=parameter(description="If only you want to see the info.",default=False)):
        '''Sends light weight information about the pokemon'''
        try:
            existingaliases = (db.field(
                "SELECT Aliases from guilds WHERE GuildID = ?", ctx.guild.id)).split(";")
            existingsprites = (db.field(
                "SELECT AliSprites from guilds WHERE GuildID = ?", ctx.guild.id)).split("|")
            if pokemon in existingaliases:
                index = existingaliases.index(pokemon)
                pokemon = existingsprites[index]
            else:
                pass
        except AttributeError:
            pass
        *_, pokemon = await convert_string_sprite_to_structured(pokemon, ctx)
        pokemon = pokemon.lower()
        pokemon = pokemon.replace(" ", "")
        if pokemon=="random":
            pokemon=random.choice(pokemon_names)
        try:
            pokemon_dict = pokedex_dict[pokemon]
        except KeyError:
            try:
                name = difflib.get_close_matches(pokemon, pokedex_dict.keys(),n=1)
                if not len(name):
                    return await ctx.send("Looks like the pokemon you requested doesn't exist...")
                name=name[0]
                pokemon_dict = pokedex_dict[name]

            except:
                return await ctx.send("You've sent an incorrect spelling or a wrong pokemon name")
        embed = await get_pokedex_stuff(pokemon_dict, True)
        embed=await embed_this_please(embed)
        await ctx.send(embed=embed,ephemeral=private)

    @lite_dex.autocomplete("pokemon")
    async def auto_ldex(self,interaction,current:str):
        return [
        app_commands.Choice(name=pokemon, value=pokemon)
        for pokemon in pokemon_names_disp if current.lower() in pokemon.lower()
    ][:25]
    @commands.hybrid_command(name='artwork', aliases=['art'],extras={"url":"artworks"})
    @app_commands.describe(pokemon="The Pokemon you want to get the artwork of",private="If only you want to see the artwork")
    async def artwork(self, ctx, *, pokemon: str=parameter(description="The Pokemon you want to see the artwork of."),private:Optional[bool]=parameter(description="If only you want to see the artwork. Only slash commands.",default=False)):
        '''Sends the official artwork of the mentioned pokemon'''
        #return await ctx.send("There have been some inconsistencies with the artwork URLs recently. The bot developer is working hard to resolve these. Try and support him through https://buymeacoffee.com/Zabbs \n Sorry for the inconvenience.")
        pokemon = pokemon.lower()
        pokemon = pokemon.replace(" ", "")
        if pokemon=="random":
            pokemon=random.choice(pokemon_names)
        try:
            url = pokedex_dict[pokemon]["url"]
        except KeyError:
            try:
                name = difflib.get_close_matches(pokemon, pokedex_dict.keys(),n=1)
                if not name:
                    return await ctx.send("Looks like the pokemon you requested doesn't exist...")
                url = pokedex_dict[name[0]]
                try:
                    url=url["url"]
                except:
                    return await ctx.send("I couldn't find the artwork for that pokemon")
            except:
                return await ctx.send("You've sent an incorrect spelling or a wrong pokemon name")
        embed=discord.Embed()
        embed.set_image(url=serebii+url+".png")
        #embed.set_footer(text="Please report any wrong artworks using the `feedback` command!")
        embed=await embed_this_please(embed)
        await ctx.send(embed=embed,ephemeral=private)

    @artwork.autocomplete("pokemon")
    async def auto_artwork(self,interaction,current:str):
        return [
        app_commands.Choice(name=pokemon, value=pokemon)
        for pokemon in pokemon_names_disp  if current.lower() in pokemon.lower()
    ][:25]
    @commands.hybrid_command(name='move',extras={"url":"moves"})
    @app_commands.describe(move="The move you want to get information on",private="If only you want to see the info.")
    async def moveinfo(self, ctx, *, move: str=parameter(description="The move you want to see the info on."),private:Optional[bool]=parameter(description="If only you want to see it. Only slash commands.",default=False)):
        '''Sends move info about the requested move'''
        move = move.lower()
        move = move.replace(" ", "")
        try:
            move_dict = moves_dict[move]
            name=move
        except KeyError:
            try:
                name = difflib.get_close_matches(move, moves_dict.keys())[0]
                if not name:
                    return await ctx.send("Looks like the move you requested doesn't exist...")
                move_dict = moves_dict[name]
            except:
                return await ctx.send("You've sent an incorrect spelling or a wrong move name")
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
            f"[Bulbapedia](https://bulbapedia.bulbagarden.net/wiki/{underscorename}_(move%29)")
        hyphenname = (name.replace(" ", "-")).lower()
        urllist.append(f"[PokemonDB](https://pokemondb.net/move/{hyphenname})")
        urllist.append(
            f"[Smogon](https://www.smogon.com/dex/ss/moves/{hyphenname}/)")
        flavourmmm = move_dict["flavourText"][-1]
        nospacename = (name.replace(" ", "")).lower()
        if flavourmmm == 'This move can\u2019t be used. It\u2019s recommended that this move is forgotten. Once forgotten, this move can\u2019t be remembered.':
            flavourmmm = move_dict["flavourText"][-2]
            urllist.append(
                f"[Serebii](https://www.serebii.net/attackdex-sm/{nospacename}.shtml)")
        else:
            urllist.append(
                f"[Serebii](https://www.serebii.net/attackdex-swsh/{nospacename}.shtml)")
        if not flavourmmm:
            flavourmmm = "\u200b"
        urllist.append(
            f"[Showdown!](https://dex.pokemonshowdown.com/moves/{nospacename})")
        embed = await convert_move_to_embed(name, move_dict, flavourmmm)
        embed.add_field(name='External Resources',
                        value=" • ".join(urllist), inline=False)
        embed=await embed_this_please(embed)
        await ctx.send(embed=embed,ephemeral=private)
    
    @moveinfo.autocomplete("move")
    async def auto_move(self,interaction,current:str):
        return [app_commands.Choice(name=move.replace("-"," ").capitalize(), value=move) for move in move_names if current.lower() in move.lower()][:25]
    @commands.hybrid_command(name='moveset',extras={"url":"movesets"})
    @app_commands.describe(pokemon="The Pokemon you want to get the moveset of",game_name="The game you want to get the moveset of",learn_type="The learning method of the moves",private="If only you want to see the moveset")
    async def moveset(self,ctx,pokemon:str=parameter(description="The Pokemon you want to see the moveset of."),game_name:str=parameter(description="The name of the game. Eg. Omega Ruby or use initials like ORAS"),learn_type:str=parameter(description="The learning method you want to see the moveset of.",default='level-up'),private:Optional[bool]=parameter(description="If only you want to see the moveset. Slash commands only.",default=False)):
        '''Sends the pokemon's moveset in the requested game. See [prefix]help moveset for more info'''
        pokemon = pokemon.lower()
        pokemon = pokemon.replace(" ", "")
        try:
            colour=pokedex_dict[pokemon]["color"]
            name=pokedex_dict["pokemon"]["name"]
            number = pokedex_dict[pokemon]["num"]
        except KeyError:
            try:
                name = difflib.get_close_matches(pokemon, pokedex_dict.keys(),n=1)[0]
                if not len(name):
                    return await ctx.send("Looks like the pokemon you requested doesn't exist...")
                number = pokedex_dict[name]["num"]
                colour=pokedex_dict[name]["color"]
            except:
                return await ctx.send("You've sent an incorrect spelling or a wrong pokemon name")
        game_name=game_name.lower()
        version_num=initial_dict.get(game_name,None)
        if version_num is None:
            version_num=difflib.get_close_matches(game_name,version_dict.keys(),n=1,cutoff=0.3)
            if not len(version_num):
                raise KeyError("I couldn't find the game you're looking for...")
            game_name=version_num[0].split("-")
            version_num=version_dict[version_num[0]]
        else:
            keys=tuple(version_dict.keys())
            values=tuple(version_dict.values()).index(version_num)
            game_name=keys[values].split("-")
        learn_type_redefined=difflib.get_close_matches(learn_type,learn_list.keys(),n=1,cutoff=0.1)
        if not len(learn_type_redefined):
            raise KeyError("I couldn't find the move learning method you're looking for...")
        movemethod=learn_type_redefined[0]
        learn_type_redefined=str(learn_list[learn_type_redefined[0]]["id"])
        try:
            e=deepcopy(movesets[str(number)][version_num][learn_type_redefined])
        except:
            return await ctx.send("The Pokemon you sent probably does not exist in that game or it does learn any moves through that method.")
        bylevel={}
        if e[0].get("level","jfioewjfo")=="jfioewjfo":
            e=deepcopy(movesets[str(number)][str(int(version_num)-1)][learn_type_redefined])
        for d in e:
            l=d.get("level",1)
            ls=bylevel.get(l,[])
            if d.get("level","jfioewjfo")!="jfioewjfo":
                d.pop("level")
            ls.append(d)
            bylevel.update({l:ls})
        colour=discord.Color.from_rgb(*colour)
        embed=discord.Embed(title=f'{name.capitalize()}',description=f'Move method - {" ".join([e.capitalize() for e in movemethod.split("-")])} \n Game - {", ".join(e.capitalize() if len(e.split())==0 else " ".join([i.capitalize() for i in e.split(" ")]) for e in game_name)}',colour=colour)
        for k,v in bylevel.items():
            n=[]
            for i in v:
                n.append(" ".join([e.capitalize() for e in moveid_dict[i['move_id']].split("-")]))
                name=f"Level {k}" if k!=0 else "Level not applicable"
            embed.add_field(name=name,value=", ".join(n),inline=False)
        embed=await embed_this_please(embed)
        return await ctx.send(embed=embed,ephemeral=private)
    
    @moveset.autocomplete("pokemon")
    async def moveset_pokemon_auto(self,interaction,current):
        return [
        app_commands.Choice(name=pokemon, value=pokemon)
        for pokemon in pokemon_names_disp  if current.lower() in pokemon.lower()
    ][:25]
    @moveset.autocomplete("game_name")
    async def moveset_gamename_auto(self,interaction,current):
        return [
        app_commands.Choice(name=e,value=e)
        for e in version_names if current.lower() in e.lower()
    ][:25]
    @moveset.autocomplete("learn_type")
    async def moveset_learntype_auto(self,interaction,current):
        return [
        app_commands.Choice(name=e.capitalize().replace("-"," "),value=e)
        for e in learn_list.keys() if current.lower() in e.lower()
    ][:25]
    
    
    @commands.hybrid_command(name='evo',aliases=['evolution','evol'],extras={"url":"evolution-chains"})
    @app_commands.describe(pokemon="The Pokemon you want to get the evolution chain on",private="If only you want to see the info.")
    async def evolution(self,ctx:commands.Context,*,pokemon:str=parameter(description="The Pokemon you want to see the evolution chain of."),private:Optional[bool]=parameter(description="If only you want to see it. Slash commands only.",default=False)):
        '''Fetch the evolution chain of a Pokemon'''
        pokemon = pokemon.lower()
        pokemon = pokemon.replace(" ", "")
        if pokemon=="random":
            pokemon=random.choice(pokemon_names)
        try:
            pokemon_id=pokedex_dict[pokemon]["num"]
            colour=pokedex_dict[pokemon]["color"]
        except:
            close=difflib.get_close_matches(pokemon,pokedex_dict.keys(),n=1)
            if not len(close):
                return await ctx.send("The Pokemon you've sent doesn't exist")
            close=close[0]
            pokemon_id=pokedex_dict[close]['num']
            colour=pokedex_dict[close]["color"]
        if pokemon_id<=0:
            return await ctx.send("Fakemons aren't available")
        try:evol_line=evol_lines[str(pokemon_id).lower()]
        except KeyError:return await ctx.send("That Pokemon doesn't have an evolution!")
        all_stuff=[deepcopy(evol_dict[d]) for d in evol_line[1:]]
        evol_line_but_keys=[id_dict[e][0] for e in evol_line]
        evol_line=[id_dict[e][1] for e in evol_line]        
        embed=discord.Embed(title='Evolution Chain',colour=discord.Color.from_rgb(*colour))
        for i,hmm in enumerate(all_stuff):
            hmm=hmm[0]
            evolves_to=evol_line[i+1]
            evolves_from=pokedex_dict[evol_line_but_keys[i+1]]["prevo"]
            hmm:dict=hmm
            overworld_rain=False
            upside_down=False
            trig_id=hmm["evolution_trigger_id"]
            if hmm["needs_overworld_rain"]:
                overworld_rain=True
            elif hmm["turn_upside_down"]:
                upside_down=True
            hmm.pop("evolution_trigger_id")
            hmm.pop("needs_overworld_rain")
            hmm.pop("id")
            hmm.pop("turn_upside_down")
            l=[]
            if trig_id==1:
                l=["Level up and"]
                for k,v in hmm.items():
                    if k=="relative_physical_stats":
                        if v==0:
                            l.append("Attack Stat=Defense Stat")
                        elif v>0:
                            l.append("Attack Stat>Defense Stat")
                        elif v<0:
                            l.append("Attack Stat<Defense Stat")
                    elif k=="minimum_level":
                        l.append(f"Minimum level needs to be {v}")
                    elif k=="minimum_happiness":
                        l.append(f"Minimum happiness has to be {v}")
                    elif k=="known_move_id":
                        move:str=moveid_dict[v]
                        move=move.replace('-'," ")
                        move=move.capitalize()
                        l.append(f"Should know move - {move}")
                    elif k=="minimum_beauty":
                        l.append(f"Minimum beauty needs to be {v}")
                    elif k=="minimum_affection":
                        l.append(f"Minimum affection needs to be {v}")
                    elif k=="time_of_day":
                        l.append(f"Time of day has to be {v.capitalize()}")
                    elif k=="location_id":
                        l.append(f"Location has to be {location_dict[str(v)]}")
                    elif k=="gender_id":
                        l.append(f"Gender has to be {'Male' if v==2 else 'Female'}")
                    elif k=="known_move_type_id":
                        l.append(f'The Pokemon should know a {type_dict[v][0]} move')
                    elif k=="held_item_id":
                        name=(item_id_dict[str(v)]).capitalize()
                        name=name.replace("-"," ")
                        l.append(f'The Pokemon needs to hold {name}')
                    elif k=="party_type_id":
                        l.append(f"There has to be a {type_dict[v][0]} Pokemon in the party")
                    elif k=="party_species_id":
                        l.append(f"A {id_dict[str(v)][1]} has to be present in the party")
            elif trig_id==2:
                if not hmm.items():
                    l=["Trade"]
                else:l=["Trade and"]
                for k,v in hmm.items():
                    if k=="held_item_id":
                        name=(item_id_dict[str(v)]).capitalize()
                        name=name.replace("-"," ")
                        l.append(f'The Pokemon needs to hold {name}')
                    elif k=="trade_species_id":
                        l.append(f"A {id_dict[str(v)][1]} has to be present in the party")
            elif trig_id==3:
                if not hmm.items():
                    l=['Use item']
                for k,v in hmm.items():
                    if k=='trigger_item_id':
                        name=(item_id_dict[str(v)]).capitalize()
                        name=name.replace("-"," ")
                        l.append(f'{name} needs to be used')
                    if k=="gender_id":
                        l.append(f"Gender has to be {'Male' if v==2 else 'Female'}")
            elif trig_id==4:
                l.append("There needs to be a Poke Ball in the bag and \nthere also needs to be an empty slot in the party")
            elif trig_id==5:
                l.append("Select a sweet of your choice and give it to the Pokemon \n Then spin your in game avatar around.")
            elif trig_id==6:
                l.append("Train in the Tower of Darkness")
            elif trig_id==7:
                l.append("Train in the Tower of Waters")
            elif trig_id==8:
                l.append("Land three critical hits in a battle")
            elif trig_id==9:
                l.append("Go somewhere and take damage")
            if overworld_rain:
                l.append("It needs to be raining in the overworld")
            if upside_down:
                l.append("You need to flip the console upside-down")
            embed.add_field(name=f"{evolves_from} ➔ {evolves_to}",value="\n".join(l))
        embed=await embed_this_please(embed)
        return await ctx.send(embed=embed,ephemeral=private)
    
    @evolution.autocomplete("pokemon")
    async def auto_evo_pokemon(self,interaction,current:str):
        return [
        app_commands.Choice(name=pokemon, value=pokemon)
        for pokemon in pokemon_names_disp  if current.lower() in pokemon.lower()
        ][:25]
    @commands.command(name='comparestats',aliases=['comp_stat','stats_diff','cstats','compstat'],hidden=True)
    async def compare_stats(self,ctx:commands.Context,*pokemon:commands.clean_content):
        
        embed=discord.Embed(title='Stats comparison')
        not_found=[]
        new_list=[]
        for poke in pokemon:
            pok = poke.lower()
            pok = pok.replace(" ", "")
            if pok not in pokemon_names:
                close=difflib.get_close_matches(pok,pokemon_names,n=1)
                if not len(close):
                    not_found.append(pok)
                    continue
                pok=close[0]
            new_list.append(pok)
        new_list=list(set(new_list))
        if len(new_list)==1 or len(new_list)>10:
            return await ctx.send("Please provide more than two Pokemon names and a maximum of 10")
        for pok in new_list:
            stats = []
            total = 0
            # pok = pok.lower()
            # pok = pok.replace(" ", "")
            # try:
            #     stats_dict=pokedex_dict[pok]["baseStats"]
            # except:
            #     close=difflib.get_close_matches(pok,pokedex_dict.keys(),n=1)
            #     if not len(close):
            #         not_found.append(pok)
            #     pok=close[0]
            #     stats_dict=pokedex_dict[pok]['baseStats']
            stats_dict=pokedex_dict[pok]["baseStats"]
            for stat_name, value in stats_dict.items():
                stats.append(f"**{stat_name}**: {value}")
                total = total + value
            stats.append(f"**Total**: {total}")
            stats = ", ".join(stats)
            embed.add_field(name=pok.replace("-"," ").capitalize(),value=stats,inline=False)
        if (x:=len(not_found)):
            if x==1:
                embed.add_field(name='Could not find a close match for this Pokemon :',value=', '.join(not_found))
            else:
                embed.add_field(name='Could not find a close match for these Pokemon name(s) :',value=', '.join(not_found))
            
        embed=await embed_this_please(embed)
        await ctx.send(embed=embed)
        
    @tasks.loop(minutes=5)
    async def cleanup_gc(self):
        gc.collect()
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{Pokemon.__qualname__} up")
    
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        #if message.content.split()[2].lower()=="sprite":return
        if message.author.bot:return 
        if message.guild is None:
            strings = []
            string = message.content
            while len(re.split("[\*_]", string, maxsplit=2)) > 1:
                e = re.split("[\*_]", string, maxsplit=2)
                strings.append(e[1])
                string = " ".join(e[1:])
            strings = strings[:4]
            for content in strings:
                try:
                    sprite_command = self.bot.get_command('sprite')
                    ctx: commands.Context = await self.bot.get_context(message)
                    await ctx.invoke(sprite_command, sprite_name=content)
                except:
                    pass
        elif message.guild.id != 336642139381301249:
            strings = []
            string = message.content
            while len(re.split("[\*_]", string, maxsplit=2)) > 1:
                e = re.split("[\*_]", string, maxsplit=2)
                strings.append(e[1])
                string = " ".join(e[1:])
            strings = strings[:4]
            for content in strings:
                try:
                    sprite_command = self.bot.get_command('sprite')
                    ctx: commands.Context = await self.bot.get_context(message)
                    await ctx.invoke(sprite_command, sprite_name=content)
                except:
                    pass


async def setup(bot):
    await bot.add_cog(Pokemon(bot))

