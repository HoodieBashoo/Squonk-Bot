import subprocess
import os
import sys
sys.path.append("..")

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

async def update(client, message):
    if message.author.id == botinfo.owner_id:
        await message.channel.send("Restarting...")
        #subprocess.run([botinfo.updater_location])
        subprocess.run([botinfo.udpater_location], stdout = subprocess.DEVNULL)
        #os.system(botinfo.updater_location)
        await client.close()
    else:
        await message.channel.send("You do not have permission to do this")