import discord

import botinfo
import command_handler
import prompt_handler
import guildprefs

intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    for guild in client.guilds:
        guildprefs.initialize_guild(guild.id)

    print("client ready!")

@client.event
async def on_guild_join(guild):
    guildprefs.initialize_guild(guild.id)

@client.event
async def on_message(message):
    if message.author.id == client.user.id:
        return
    if message.guild.id != botinfo.squonk_id:
        print("Message was not in the right server")
        return
    if client.user.mentioned_in(message):
        await message.channel.send(botinfo.description + f" My prefix is {guildprefs.get_guild_pref(message.guild.id, 'prefix')}")
        return

    prompt = prompt_handler.find_prompt(message.channel.id)
    if prompt is not None:
        await message.channel.send("found active prompt in this channel")
        if prompt.author == message.author:
            await message.channel.send("message author is the same as prompt author")
            await prompt_handler.process_satisfaction(message)

    server_prefix = guildprefs.get_guild_pref((message.guild.id), "prefix")
    if message.content.startswith(server_prefix):
        await command_handler.process_command(message, server_prefix)

client.run(botinfo.bot_token)