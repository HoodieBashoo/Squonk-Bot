import sys
sys.path.append("..")

import guildprefs
import botinfo
import prompt_handler

async def update_prefix(message, new_prefix, send_channel):
    if (message.author.id != botinfo.owner_id):
        await message.channel.send(f"Only the bot owner can use this command until a proper permission system is set up")
        return

    if new_prefix == "":
        await send_channel.send("Command requires a new prefix")
        return
    if new_prefix.find(" ") > -1:
        await send_channel.send("Unable to use prefixes that contain spaces yet")
        return

    guildprefs.edit_guild_pref(message.guild.id, "prefix", new_prefix)
    await send_channel.send(f"Updated prefix to {new_prefix}")

async def userlog(message):
    if (message.author.id != botinfo.owner_id):
        await message.channel.send(f"Only the bot owner can use this command until a proper permission system is set up")
        return

    guild = message.guild
    if guildprefs.get_guild_pref(guild.id, "userlog") == True:
        await prompt_handler.start_prompt(message.author, message.guild, message.channel, "userlog", "enabled")
    else:
        await prompt_handler.start_prompt(message.author, message.guild, message.channel, "userlog", "disabled")

async def pinboard(message):
    if (message.author.id != botinfo.owner_id):
        await message.channel.send(f"Only the bot owner can use this command until a proper permission system is set up")
        return

    guild = message.guild
    if guildprefs.get_guild_pref(guild.id, "pinboard") == True:
        await prompt_handler.start_prompt(message.author, message.guild, message.channel, "pinboard", "enabled")
    else:
        await prompt_handler.start_prompt(message.author, message.guild, message.channel, "pinboard", "disabled")