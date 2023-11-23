import subprocess
import os
import time, datetime
import sys
sys.path.append("..")

import discord

import botinfo
import guildprefs
import prompt_handler
from prompts import helpinfo

async def shutdown(client, message):
    if message.author.id == botinfo.owner_id:
        await message.channel.send("Shutting down...")
        await client.close()
    else:
        await message.channel.send("You do not have permission to do this")

async def help(client, message, parameter):
    if (parameter == ""):
        await prompt_handler.start_prompt(client, message.author, message.guild, message.channel, "help", "")
    else:
        match parameter:
            case "all":
                embeds = helpinfo.all_embeds()
                for embed in embeds:
                    await message.channel.send(embed=embed)
            case "config":
                await message.channel.send(embed=helpinfo.config_embed())
            case "utility":
                await message.channel.send(embed=helpinfo.utility_embed())

async def ping(client, message):
    colour = None
    print(round(client.latency * 1000))
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
        description=botinfo.description,
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
        await message.channel.send("Restarting...")
        subprocess.Popen([botinfo.updater_location])
        await client.close()
    else:
        await message.channel.send("You do not have permission to do this")

async def prefs_update(client, message):
    if (message.author.id != botinfo.owner_id):
        return
    guildprefs.update_guild_pref_data(client)

def on_start(time):
    global start_time
    start_time = time

def get_uptime():
    current_time = time.time()
    difference = int(round(current_time - start_time))
    uptime = datetime.timedelta(seconds=int(round(time.time() - start_time)))
    days, hours, minutes = uptime.days, uptime.seconds // 3600, uptime.seconds % 3600 // 60
    seconds = uptime.seconds - hours * 3600 - minutes * 60
    uptime = f"{days}d{hours:02d}h{minutes:02d}m{seconds:02d}s"
    return uptime