import subprocess
import time
import datetime
import sys
sys.path.append("..")

import discord

import botinfo
import guildprefs
import prompt_handler
from prompts import helpinfo


start_time = 0

async def shutdown(client, message):
    if message.author.id == botinfo.owner_id:
        await message.channel.send("Shutting down...")
        await client.close()
    else:
        await message.channel.send("You do not have permission to do this")

async def help(client, message, parameter):
    if parameter == "":
        await prompt_handler.start_prompt(client, message.author, message.guild, message.channel, "help", "")
    else:
        match parameter:
            case "all":
                embeds = helpinfo.all_embeds()
                await message.channel.send(embeds=embeds)
            case "config":
                await message.channel.send(embed=helpinfo.config_embed())
            case "utility":
                await message.channel.send(embed=helpinfo.utility_embed())

async def ping(client, message):
    if round(client.latency * 1000) <= 150:
        colour = discord.Colour.green()
    elif round(client.latency * 1000) <= 200:
        colour = discord.Colour.yellow()
    elif round(client.latency * 1000) <= 250:
        colour = discord.Colour.orange()
    elif round(client.latency * 1000) <= 350:
        colour = discord.Colour.red()
    else:
        colour = discord.Colour.dark_purple()

    embed = discord.Embed(
        description=f"poing :O `{round(client.latency * 1000)}ms`",
        colour=colour
    )
    await message.channel.send(embed=embed)

async def info(message):
    uptime = get_uptime()
    prefix = guildprefs.get_guild_pref(message.guild.id, "prefix")
    creation_date = datetime.datetime(2023, 10, 16, 10, 28)
    embed = discord.Embed(
        title="Info",
        description=f"{botinfo.description}\n"
                    f"Image assets were made by the amazing Lync5",
        colour=discord.Colour.orange()
    )
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/384064317722722305/1177015150721638531/SquonkBotAvatar.png?ex=6570f7c7&is=655e82c7&hm=0be0839cadeac70a2e80499f5e42a402147056fd71e0f853dc5516cccb952053&")
    embed.add_field(name="Prefix", value=prefix, inline=True)
    embed.add_field(name="Uptime", value=uptime, inline=True)
    embed.set_footer(text="Created by HoodieBashoo", icon_url="https://cdn.discordapp.com/attachments/384064317722722305/1177027507787149364/a9a71e166f0e00488a994240c4af7782.png?ex=65710349&is=655e8e49&hm=3016cdec48af9275f1b5d28417e66c35a953314a8076798f5acf63c122cd0416&")
    embed.timestamp = creation_date
    await message.channel.send(embed=embed)

async def update(client, message):
    if message.author.id == botinfo.owner_id:
        if botinfo.updater_location is None:
            await message.channel.send("No updater found")
            return
        await message.channel.send("Restarting...")
        subprocess.Popen([botinfo.updater_location])
        await client.close()
    else:
        await message.channel.send("You do not have permission to do this")

async def display_preferences(client, message):
    preferences = guildprefs.get_guild_prefs(message.guild.id)

    if preferences["userlog"]:
        userlog_info = f"Enabled in <#{preferences['userlog_channel']}>"
    else:
        userlog_info = "Disabled"

    if preferences["pinboard"]:
        try:
            emoji_object = client.get_emoji(int(preferences["pin_activation_emoji"]))
        except ValueError:
            emoji_object = preferences["pin_activation_emoji"]
        pinboard_info = f"Enabled in <#{preferences['pinboard_channel']}> with {emoji_object}"
    else:
        pinboard_info = f"Disabled"

    if preferences["twithelper"]:
        twitter_info = f"Active with buttons visible for {preferences['twitter_button_time']} seconds"
    else:
        twitter_info = "Inactive"

    embed = discord.Embed(
        title="Preferences",
        description="Server preferences can be changed with commands in the config section",
        colour=discord.Colour.orange()
    )
    embed.set_thumbnail(
        url="https://cdn.discordapp.com/attachments/384064317722722305/1179577092405473350/Preferences.png?ex=657a49c6&is=6567d4c6&hm=8b7794e03d1e039cd73f58ab7e0f1d9bae1b9aaedc5ddceb30ed8a5bceb8fcd2&")
    embed.add_field(name="Prefix", value=preferences["prefix"], inline=True)
    embed.add_field(name="Userlog", value=userlog_info, inline=True)
    embed.add_field(name="", value="", inline=False)
    embed.add_field(name="Pinboard", value=pinboard_info, inline=True)
    embed.add_field(name="Twitter Helper", value=twitter_info, inline=True)

    await message.channel.send(embed=embed)

async def prefs_update(client, message):
    if message.author.id != botinfo.owner_id:
        return
    guildprefs.update_guild_pref_data(client)

def on_start(t):
    global start_time
    start_time = t

def get_uptime():
    uptime = datetime.timedelta(seconds=int(round(time.time() - start_time)))
    days, hours, minutes = uptime.days, uptime.seconds // 3600, uptime.seconds % 3600 // 60
    seconds = uptime.seconds - hours * 3600 - minutes * 60
    uptime = f"{days}d{hours:02d}h{minutes:02d}m{seconds:02d}s"
    return uptime
