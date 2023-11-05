import discord

import botinfo
import commands

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
    if message.content.startswith(botinfo.prefix):
        await commands.process_command(message)

client.run(botinfo.bot_token)