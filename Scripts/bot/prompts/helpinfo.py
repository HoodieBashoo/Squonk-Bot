import discord

from prompts import prompt_urls


def all_embeds():
    embeds = [
        config_embed(),
        utility_embed()
    ]
    return embeds

def config_embed():
    embed = discord.Embed(
        title="Config Commands",
        description="__prefix/updateprefix__\n"
                    "- Change the prefix required for commands\n"
                    "1 Argument for the prefix\n"
                    "\n"
                    "__userlog__\n"
                    "- Configure a channel for updates on members joining and leaving\n"
                    "0 Arguments",
        colour=discord.Colour.orange()
    )
    embed.set_thumbnail(url=prompt_urls.config_icon)
    return embed

def utility_embed():
    embed = discord.Embed(
        title="Utility Commands",
        description="__help__\n"
                    "- Info on available commands\n"
                    "1 Argument for the category\n"
                    "0 Arguments for prompt\n"
                    "\n"
                    "__ping__\n"
                    "- Check how quickly the bot responds!\n"
                    "0 Arguments\n"
                    "\n"
                    "__shutdown__\n"
                    "- Owner only\n"
                    "0 Arguments\n"
                    "\n"
                    "__update__\n"
                    "- Owner Only\n"
                    "0 Arguments",
        colour=discord.Colour.orange()
    )
    embed.set_thumbnail(url=prompt_urls.utility_icon)
    return embed