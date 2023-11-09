import discord

import botinfo
import command_handler
import prompt_handler
import guildprefs
import userlog


intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    for guild in client.guilds:
        guildprefs.initialize_guild(guild.id)

    # TODO: Not sure if this is necessary, further testing required
    prompt_handler.reset()

    print("client ready!")

@client.event
async def on_guild_join(guild):
    guildprefs.initialize_guild(guild.id)

@client.event
async def on_member_join(member):
    await userlog.member_joined(member)

@client.event
async def on_member_remove(member):
    await userlog.member_left(member)

@client.event
async def on_member_ban(guild, member):
    await userlog.member_banned(guild, member)

@client.event
async def on_member_unban(guild, member):
    await userlog.member_unbanned(guild, member)

@client.event
async def on_message(message):
    if message.author.id == client.user.id:
        return
    if client.user.mentioned_in(message):
        await message.channel.send(botinfo.description + f" My prefix is {guildprefs.get_guild_pref(message.guild.id, 'prefix')}")
        return

    prompt = prompt_handler.find_prompt(message.channel.id)
    if prompt is not None:
        if prompt.author == message.author:
            await prompt_handler.process_satisfaction(message)

    server_prefix = guildprefs.get_guild_pref((message.guild.id), "prefix")
    if message.content.startswith(server_prefix):
        await command_handler.process_command(client, message, server_prefix)

client.run(botinfo.bot_token)