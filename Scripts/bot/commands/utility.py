import subprocess
import os
import sys
sys.path.append("..")

import discord

import botinfo
import prompt_handler
from prompts import helpinfo

async def shutdown(client, message):
    if message.author.id == botinfo.owner_id:
        await message.channel.send("Shutting down...")
        await client.close()
    else:
        await message.channel.send("You do not have permission to do this")

async def help(message, parameter):
    if (parameter == ""):
        await prompt_handler.start_prompt(message.author, message.guild, message.channel, "help", "")
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
    elif round(client.latency * 1000) <= 300:
        colour = discord.Colour.red()
    else:
        colour = discord.Colour.dark_purple()

    embed = discord.Embed(
        description=f"poing :O `{round(client.latency * 1000)}ms`",
        colour=colour
    )
    await message.channel.send(embed=embed)

async def update(client, message):
    if message.author.id == botinfo.owner_id:
        await message.channel.send("Restarting...")
        subprocess.Popen([botinfo.updater_location])
        #subprocess.run([botinfo.updater_location], stdout = subprocess.DEVNULL)
        #os.system(botinfo.updater_location)
        await client.close()
    else:
        await message.channel.send("You do not have permission to do this")