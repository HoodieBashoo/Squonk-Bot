import discord

from prompts import prompt_urls


def all_embeds():
    embeds = [
        utility_embed(),
        config_embed()
    ]
    return embeds

def config_embed():
    embed = discord.Embed(
        title="Config Commands",
        description="""
__prefix/updateprefix__
- Change the prefix required for commands
1 Argument for the prefix

__userlog__
- Configure a channel for updates on members joining and leaving
0 Arguments

__pinboard__
- Configure a channel to send pinned messages to!
- React with the specified emoji or use the built-in pin button to utilize this feature
0 Arguments

__twithelper__
- Enable or disable an automatic twitter embed fixer
0 Arguments
        """,
        colour=discord.Colour.orange()
    )
    embed.set_thumbnail(url=prompt_urls.config_icon)
    return embed

def utility_embed():
    embed = discord.Embed(
        title="Utility Commands",
        description="""
__help__
- List of available commands
1 Argument for the category
0 Arguments for prompt

__info__
- Info about me
0 Arguments

__preferences__
- Current preferences in this server
0 Arguments

__ping__
- See how quickly I respond!
0 Arguments
        """,
        colour=discord.Colour.orange()
    )
    embed.set_thumbnail(url=prompt_urls.utility_icon)
    return embed