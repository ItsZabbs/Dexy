<head><link rel="shortcut icon" type="image/x-icon" href="https://cdn.discordapp.com/avatars/853556227610116116/8efe9df25de5cdb5bc90232797032ef6.png"></head>
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

## Evolution Chains

## Items

## Pokedex

## Lite Pokedex

## Type matchup calculations
# Miscellaneous

- Bulleted
- List

1. Numbered
2. List

**Bold** and _Italic_ and `Code` text

[Link](url) and ![Image](src)

For more details see [Basic writing and formatting syntax](https://docs.github.com/en/github/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax).

### Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/ItsZabbs/Pokedex-Bot/settings/pages). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Commands
placeholder for commands
Having trouble with Pages? Check out our [documentation](https://docs.github.com/categories/github-pages-basics/) or [contact support](https://support.github.com/contact) and we’ll help you sort it out.
