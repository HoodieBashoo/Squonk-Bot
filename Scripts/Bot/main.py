import discord

import botinfo
import commands
import guildprefs


intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("client ready!")
    
@client.event
async def on_message(message):
    if message.author.id == client.user.id:
        return
    if message.guild.id != botinfo.squonk_id:
        print("Message was not in the right server")
        return
    server_prefix = guildprefs.get_guild_pref((message.guild.id), "Prefix")
    if message.content.startswith(server_prefix):
        await commands.process_command(message)

client.run(botinfo.bot_token)