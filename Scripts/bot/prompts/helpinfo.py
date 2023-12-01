import discord


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
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/384064317722722305/1176579447101607936/Config.png?ex=656f61ff&is=655cecff&hm=6051cb3422ec8c19bc07c644393be4dd3d2a42e320731e53ddf8adb6ea401fab&")
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
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/384064317722722305/1176579467464937492/Settings.png?ex=656f6204&is=655ced04&hm=971520842a0c2b48ed201f36bb946f6d627240116b8cae303abcece0f94b32f3&")
    return embed
