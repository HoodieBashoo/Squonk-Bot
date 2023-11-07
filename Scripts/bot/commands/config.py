import sys
sys.path.append("..")

import guildprefs
import prompt_handler

async def update_prefix(guild_id, new_prefix, send_channel):
    if new_prefix == "":
        await send_channel.send("Command requires a new prefix")
        return
    if new_prefix.find(" ") > -1:
        await send_channel.send("Unable to use prefixes that contain spaces yet")
        return

    guildprefs.edit_guild_pref(guild_id, "prefix", new_prefix)
    await send_channel.send(f"Updated prefix to {new_prefix}")

async def userlog(message):
    guild = message.guild
    if guildprefs.get_guild_pref(guild.id, "userlog") == True:
        await prompt_handler.start_prompt(message.author, message.guild, message.channel, "userlog", "enabled")
    else:
        await prompt_handler.start_prompt(message.author, message.guild, message.channel, "userlog", "disabled")