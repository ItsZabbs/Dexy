from __future__ import annotations
from typing import Any, List, Tuple, Dict, Union,TYPE_CHECKING,Iterable
from discord.ext.commands import Converter, Context,BadArgument
from ujson import load
import random
import re
import difflib
from collections import namedtuple

from ...db import db
from ...bot import Bot

pokemon_names :List[str]= load(
    open("lib/cogs/pokedexdata/pokemon_names.json", "r", encoding='utf-8'))
pokemon_names_ani:List[str]=load(open("lib/cogs/pokedexdata/pokemon_names_ani.json","r",encoding='utf-8'))
sprite_types=re.compile(r"(^| )"+r"( |^|\Z)|(^| )".join(["rs", "bw", "yellow", "gen3", "gen1", "rb", "gen5", "silver", "pt", "rg", "frlg", "dp", "gold", "bwani", "gen2", "gen5ani", "crystal", "gen4", "afd", "gen2g", "gen2s", "hgss", "dp", "pt", "gen4"])+r"( |^|\Z)")

SpritePokemon=namedtuple('SpriteInfo',['back','shiny','sprite_type','pokemon'])


def get_close_matches(argument:str,possibilities:Iterable[str],cutoff:float=0.6)->Union[str,None]:
    close=difflib.get_close_matches(argument,possibilities,n=1,cutoff=cutoff)
    return close[0] if close else None
async def get_sprite_alias(ctx:Context[Bot],argument:str)->str:
    if ctx.guild is not None:
        existingaliases,existingsprites=await db.alias_cache[ctx.guild.id]
        if existingaliases is not None and argument in existingaliases:
            return existingsprites[existingaliases.index(argument.lower())]
    return ""
if TYPE_CHECKING:
    class PokemonConverter(Converter):
        def __init__(self,names:List,closematch:bool=True)->None:
            ...
        async def convert(self,ctx:Context[Bot],argument:str)->str:
            ...
    SpriteConverter=Tuple[bool,bool,str,str]
    CustomConverter=str
else:
    class PokemonConverter(Converter):
        def __init__(self,names:List[str],closematch:bool=True,) -> None:
            super().__init__()
            self.close=closematch
            self.names=names
        async def convert(self, ctx: Context[Bot], argument: str) -> str:
            argument=argument.lower()
            if arg:=await get_sprite_alias(ctx,argument):
                *_,pokemon=convert_string_to_sprite(arg)
                pokemon.replace("-","")
                return pokemon
            *_,pokemon=convert_string_to_sprite(argument)
            if pokemon in ("random","prandom"):
                return random.choice(self.names)
            if pokemon in self.names:
                return pokemon.replace("-","")
            elif self.close:
                name=get_close_matches(pokemon,self.names)
                if name is not None:return name.replace("-","")
                raise BadArgument("Could not find that Pokemon.")
            else:
                raise BadArgument("Could not find that Pokemon."+(f" Were you looking for `{name}`?" if (name:=get_close_matches(pokemon,pokemon_names)) is not None else ""))

    class SpriteConverter(Converter):
        """Convert a string into a Sprite Named Tuple"""
        async def convert(self, ctx: Context[Bot], argument: str) -> Tuple[bool,bool,str,str]:
            argument=argument.lower()
            if arg:=await get_sprite_alias(ctx,argument):
                return convert_string_to_sprite(arg)
            else:
                back,shiny,sprite_type,pokemon=convert_string_to_sprite(argument)
                if pokemon in ("random","prandom") and sprite_type=="none":
                    return SpritePokemon(back,shiny,sprite_type,random.choice(pokemon_names_ani))
                elif pokemon in ("random","prandom"):
                    return SpritePokemon(back,shiny,sprite_type,random.choice(pokemon_names))
                if pokemon not in pokemon_names_ani and sprite_type=="none" and pokemon in pokemon_names:
                    raise BadArgument(f"That Pokemon only has a bw sprite. Try `{pokemon} bw{' back' if back else ''}{' shiny' if shiny else ''}` instead.")
                if pokemon not in pokemon_names:
                    raise BadArgument("Could not find that Pokemon."+(f" Were you looking for `{name}`" if (name:=get_close_matches(pokemon,pokemon_names)) is not None else ""))
                else:
                    return SpritePokemon(back,shiny,sprite_type,pokemon)

    class CustomConverter(Converter):
        def __init__(self,itemlist:List[str],arg_name:str) -> None:
            self.itemlist=itemlist
            self.arg_name=arg_name
        async def convert(self, ctx: Context[Bot], argument: str):
            if argument in self.itemlist:
                return argument
            else:
                arg=get_close_matches(argument,self.itemlist)
                if arg is None:
                    raise BadArgument(f"Could not find that {self.arg_name}")
                return arg
        
def convert_string_to_sprite(argument:str)->Tuple[bool,bool,str,str]:
    '''Returns the Pokemon converted into sprite formatting in the following order
    back:bool
    shiny:bool
    sprite_type:str
    pokemon_name:str
    '''
    back=False
    argument=argument.lower()
    if re.search(r"(^| )back(^| |\Z)",argument):
        argument = re.sub(r"(^| )back(^| |\Z)"," ", argument).strip()
        back=True
    shiny=False
    if re.search(r"(^| )shiny(^| |\Z)",argument):
        argument=re.sub(r"(^| )shiny(^| |\Z)"," ",argument).strip()
        shiny=True
    sprite_type="None"
    if match:=sprite_types.search(argument):
        argument=argument.replace(match.group(),"")
        sprite_type=match.group().strip().lower()
    argument=re.sub(r"(^| )gigantamax(^| |\Z)"," gmax",argument)
    argument=re.sub(r"(^| )mega (x|y)(^| |\Z)",r" mega\2",argument)
    argument=re.sub(r"(^| )female(^| |\Z)"," f",argument)
    argument=re.sub(r"(^| )hisuian(^| |\Z)"," hisui",argument)
    argument=re.sub(r"(^| )galarian(^| |\Z)"," galar",argument)
    argument=re.sub(r"(^| )paldean(^| |\Z)"," paldea",argument)
    argument=re.sub(r"(^| )alolan(^| |\Z)"," alola",argument)
    x=argument.split()
    if x[0].startswith("tapu") and len(x) > 1:
        argument = x[0] + x[1]
    elif len(x) > 1:
        argument = x[0] + "-" + "-".join(x[1:])
    else:
        argument = x[0]
    if argument!="meganium" and argument.startswith(("crowned", "origin", "dusk-mane", "duskmane", "dawnwings", "dawn-wings", "megax", "megay", "female", "galar", "alola", "mega", "gmax", "eternamax", "hisui")):
        x = argument.split("-")
        argument = x[-1] + "-" + ("".join((x[-2::-1])[::-1]))
    return SpritePokemon(back,shiny,sprite_type.lower(),argument.strip())
    