## Pokedex Bot

Pokedex Bot is a fully fledged Pokemon bot with all kinds of information necessary to competitive and leisure Pokemon players!<br />Also has features like Pokemon sprites, artworks and much more!

<br>
Find the support server here - [Support server link](https://discord.gg/FBFTYp7nnq)
<br>
Invite the bot! - [Invite link](https://discord.com/api/oauth2/authorize?client_id=853556227610116116&permissions=277092812864&scope=bot%20applications.commands)
<br>

## Features

### All Movesets
You can find movesets of **ALL POKEMON** and **all versions**!! Just use <br> dexy moveset &lt;pokemon&gt; &lt;version&gt; <br> and you'll get all learnable moves! 

### Variety of Sprites
Pokemon sprites are also available through the bot. Any game's sprite can be found. It can be any game from Red and Green to the latest games!! 

### Type Matchups
Find it tough to calculate type matchups? You can use the bot to calculate it now!! A Pokemon's weaknesses and a move's powers all through a single command!!

# Documentation guide

`<>` Indicates a required argument. You'll have to send it in order to get your desired outcome. <br>
`[]` Indicates an optional argument. You can choose to send this if you want. For example, choosing the learn type for the [moveset](#Movesets) command.<br>
`[foo|bar]` indicates the command's aliases. You can any one of these to initiate the command's output. For example, `[dex|pokedex]` indicates that you can use either `dexy dex manectric` or `dexy pokedex manectric`
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
Description- Sends the requested pokemon's moveset in the required version.
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

Version specific Sprites:
| Sprite               | Game                           |
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

The `sprite-name` follows the same syntax as the `sprite-name` in the [sprite](#sprites) commands.

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
