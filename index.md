## Pokedex Bot

Pokedex Bot is a fully fledged Pokemon bot with all kinds of information necessary to competitive and leisure Pokemon players!<br />Also has features like Pokemon sprites, artworks and much more!

Find the support server here - <a href="https://discord.gg/FBFTYp7nnq">Support server link</a>

Invite the bot! - <a href="https://discord.com/api/oauth2/authorize?client_id=853556227610116116&permissions=277092812864&scope=bot%20applications.commands">Invite link</a>

## Features

### All Movesets
You can find movesets of **ALL POKEMON** and **all versions**!! Just use <br> dexy moveset &lt;pokemon&gt; &lt;version&gt; <br> and you'll get all learnable moves! 

### Variety of Sprites
Pokemon sprites are also available through the bot. Any game's sprite can be found. It can be any game from Red and Green to the latest games!! 

### Type Matchups
Find it tough to calculate type matchups? You can use the bot to calculate it now!! A Pokemon's weaknesses and a move's powers all through a single command!!

# Documentation guide

`<>` Indicates a required argument. You'll have to send it in order to get your desired outcome. <br>
`[]` Indicates an optional argument. You can choose to send this if you want. For example, choosing the learn type for the [moveset](https://itszabbs.github.io/Pokedex-Bot#movesets) command.<br>
`[foo|bar]` indicates the command's aliases. You can use any one of these to initiate the command's output. For example, `[dex|pokedex]` indicates that you can use either `dexy dex manectric` or `dexy pokedex manectric`
###  <span style="color:red">Do not literally type out the []<>| etc.</span> 
# Pokemon related commands

## Artworks
Description- Sends the official artwork of the mentioned pokemon<br>
Command - `dexy [artwork|art] <pokemon>`
<br>`<pokemon>` can be any Pokemon, mega, gmax, or regional form. Pokemon's forms also work.
<br>Example usage:<br>
`dexy artwork Charizard` - Provides artwork of Charizard <br>
`dexy artwork Charizard mega x` - Provides artwork of Mega Charizard X <br>
`dexy artwork Manectric mega` - Provides artwork of Mega Manectric <br>
`dexy artwork Charizard Gmax` - Provides artwork of GMax Charizard <br>
`dexy artwork Meowth Alola` - Provides artwork of Alolan Meowth <br>

## Abilities
Description- Sends the ability's information with its Smogon rating <br>
Command - `dexy [ability|abil] <ability-name>`
<br>`<ability-name>` can be any Pokemon ability.
<br>Example usage:<br>
`dexy ability swift swim` - Provides the information about the Swift Swim ability and gives a Smogon based rating. 

## Moves
Description- Sends all kinds of information about a move <br>
Command - `dexy move <move-name>`
<br>`<ability-name>` can be any Pokemon move.
<br>Example usage:<br>
`dexy move lick` - Provides the information the move Lick.

## Movesets
Description- Sends the requested pokemon's moveset in the required version.<br>
Command - `dexy moveset <pokemon-name> <version-name> [learn-type]`
<br>`<pokemon-name>` can be any Pokemon name. Hyphenate megas and gmax to the name. Same with forms.
<br>`<version-name>` can be any complete version name such as `omegaruby` or can also be the version group initials `oras`.
<br>`[learn-type]` can be any learning type such as:

`tutor` for moves learnt via tutor 

`level-up` for moves learnt via levelling up

`machine` for moves learnt through technical machines

`egg` for egg moves

`form-change` for moves learnt through forme changes.

The default is `level-up`


Example Usage:

`dexy moveset manectric-mega oras machine` - Provides the learnset of Manectric Mega in Omega Ruby and Alpha Sapphire learnt through TMs<br>
`dexy moveset manectric oras` - Provides the learnset of Manectric in ORAS learnt through levelling up<br>

## Sprites

Description- Sends the ingame sprite for a Pokemon.

Command- `dexy [sprite|spr] <sprite-name>`


`<sprite-name>` can be any Pokemon name.

Add `shiny` to the Pokemon name to see the shiny sprite.

Add `back` to the Pokemon name to see the back sprite.

### You can also use bare italics to summon Pokemon names. This can be done via:

`*<pokemon name>*`

Examples- 

*Manectric shiny* - Would summon a Shiny Manectric

*Manectric back* - Would summon the back sprite of Manectric

*Manectric bwani* - Would summon the BW2 version of the sprite. 

*Manectric bwani* *Manectric* - This would summon two sprites. The animated Manectric sprite, and the BW2 version. Remember to surroud individual Pokemon names in different italics. The text in the above example is actually - `*Manectric bwani* *Manectric*`

Version specific Sprites:
| Sprite               | Corresponding Game                           |
|----------------------|--------------------------------|
| `bw` or `gen5`       | Black and White                |
| `bwani` or `gen5ani` | Black 2 and White 2            |
| `gen4` or `hgss`     | HeartGold and SoulSilver       |
| `pt`                 | Platinum                       |
| `dp`                 | Diamond and Pearl              |
| `afd`                | April Fools' Day from Showdown |
| `rb`                 | Red and Blue                   |
| `crystal`            | Crystal                        |
| `yellow` or `gen1`   | Yellow                         |
| `emerald`            | Emerald                        |
| `rs`                 | Ruby and Sapphire              |
| `frlg`               | FireRed and LeafGreen          |
| `gold`               | Gold                           |
| `silver`             | Silver                         |


## Alias Management
Description- Commands that help you manage aliases for the server.


What are aliases?

Aliases are a way to summon a Pokemon with some text other than its name.

An example would be to type `dexy sprite Zabbs` and see Manectric's sprite.

This can be super easy to do.

<span style="color:red">This requires MANAGE SERVER permissions</span>

###  <span style="color:yellow">How to add an alias-</span> 

`dexy alias add <alias-name> <sprite-name>`

The `<alias-name>` can be any text you wish to summon the sprite with. For multiple words, surround the alias-name in doublequotes.

The `sprite-name` follows the same syntax as the `sprite-name` in the [sprite](https://itszabbs.github.io/Pokedex-Bot#sprites) commands.

Example Usage-

`dexy alias add "Zabbs" manectric`

`dexy alias add "zabbs and whatever he likes" manectric`

###  <span style="color:yellow">How to remove an alias-</span> 

`dexy alias add <alias-name>`

The `<alias-name>` can be any text you've added previously.

Example Usage-

`dexy alias remove "Zabbs"`

`dexy alias remove "zabbs and whatever he likes"`

###  <span style="color:yellow">How to list all aliases-</span> 

`dexy alias list`

## Evolution Chains

Description- Sends the evolution of the mentioned pokemon<br>
Command - `dexy [evo|evolution|evol] <pokemon>`
<br>`<pokemon>` can be any Pokemon, mega, gmax, or regional form. Pokemon's forms also work.
<br>Example usage:<br>
`dexy evo Charizard` <br>
`dexy evol Charizard mega x` <br>
`dexy evolution Manectric mega` <br>
`dexy evo Charizard Gmax`<br>
`dexy evo Meowth Alola` <br>

## Items
Description- Sends information about an item <br>
Command - `dexy item <item-name>`
<br>`<item-name>` can be any Item.
<br>Example usage:<br>
`dexy item xattack` - Provides the information the item X-Attack.

## Pokedex
Description- Sends wholehearted information about a Pokemon <br>
Command - `dexy [dex|pokedex] <pokemon>`
<br>`<pokemon>` can be any Pokemon, mega, gmax, or regional form. Pokemon's forms also work.
<br>Example usage:<br>
`dexy dex Charizard` <br>
`dexy dex Charizard mega x` <br>
`dexy dex Manectric mega` <br>
`dexy dex Charizard Gmax`<br>
`dexy dex Meowth Alola` <br>
This command sends a very big embed with Type, Stats, Abilities, Gender, Evolution, Height, Weight, Smogon Tier, Egg Groups, and External resources. As a result, this command has the capability to flood chat. Look at the next command for a smaller embed.

## Lite Pokedex
Description- Sends light weight information about a Pokemon <br>
Command - `dexy [ldex|litedex|cheapdex] <pokemon>`
<br>`<pokemon>` can be any Pokemon, mega, gmax, or regional form. Pokemon's forms also work.
<br>Example usage:<br>
`dexy ldex Charizard` <br>
`dexy ldex Charizard mega x` <br>
`dexy ldex Manectric mega` <br>
`dexy ldex Charizard Gmax`<br>
`dexy ldex Meowth Alola` <br>

## Type matchup calculations
Description- Sends the type matchup calculations of a Pokemon or a Move <br>
Command - `dexy [type] <pokemon or move>`
<br>`<pokemon or move>` can be any Pokemon, mega, gmax, or regional form. Pokemon's forms also work. It can also be any move name.
<br>Example usage:<br>
`dexy type Charizard` <br>
`dexy type Charizard mega x` <br>
`dexy type Manectric mega` <br>
`dexy type Charizard Gmax`<br>
`dexy type Meowth Alola` <br>
`dexy type Play Rough` <br>
# Miscellaneous

## Prefix management
This section will describe the commands to use to set what the bot responds to

###  <span style="color:yellow">How to add a prefix-</span> 
Command- `dexy prefix add <new prefix>`

`<new prefix>` can be any characters but should not include a space or comma.

###  <span style="color:yellow">How to remove a prefix-</span> 
Command- `dexy prefix remove <old prefix>`

`<old prefix>` can be any existing prefix. Look at the nexr section on how to see all prefixes.

Note: You can remove the default prefix. Before doing so, you should ensure that the bot has another prefix set. If you remove the prefix by accident, and there is no other prefix, mentioning the bot instead of dexy will still work.
###  <span style="color:yellow">How to list all prefixes-</span> 
Command- `dexy prefix list`

This will list all prefixes separated by a comma.

## Feedback

Command- `dexy feedback <whatever you want to put here>`

Description- `Sends feedback to the bot developer. Any kind of feedback or suggestions to even bug reports are accepted.`

## Invite

Command- `dexy invite`

Description- Sends the invite link to add the bot to another server.

## About

Command- `dexy about`

Description- Sends the bot's information. This also lists any potential influences on the bot's design.

## Ping

Command- `dexy ping`

Description- Returns the bot's latency.

## Vote

Command- `dexy vote`

Description- Sends the bot's top.gg link so people can vote for it.

## Help

Command- `dexy help [command name]`

`<command name>` can be any command name. It can also be a category of commands, for example, Pokemon or Misc.

Ensure that the category name is capitalised so it is `Pokemon` and not `pokemon`.

Not sending any command name will result in an embed that lists all usable commands.
