import discord

import guildprefs


pin_emoji = "📌"

async def process_reaction(client, info):
    message = await client.get_channel(info.channel_id).fetch_message(info.message_id)
    if not is_valid(client, info, message):
        return

    # TODO: pin_emoji = guildprefs.get_guild_pref(message.guild.id, "pin_emoji")
    # set pin emoji in the prompt
    pin_reaction = discord.utils.get(message.reactions, emoji=pin_emoji)

    reactions = message.reactions
    for reaction in reactions:
        if reaction.emoji == pin_emoji:
            if reaction.count > 1 or message.channel == message.guild.get_channel(int(guildprefs.get_guild_pref(message.guild.id, "pinboard_channel"))):
                return
            else:
                break

    if pin_reaction is not None:
        await pin_message(client, message.author, message.channel, message)

async def pin_message(client, member, message_channel, message):
    channel = await get_channel_if_valid_from_member(client, member)
    name = ""
    if (member.global_name is not None):
        name = member.global_name
    else:
        name = member.name
    webhook = await channel.create_webhook(name=name)

    link = f"{message.jump_url}\n\n"
    content = f"{link}{message.content}"

    attachments = message.attachments
    files = []
    for attachment in attachments:
        file = await attachment.to_file()
        files.append(file)

    await send_message(client, member, channel, webhook, content, files)
    await webhook.delete()

async def send_message(client, member, channel, webhook, content, attachments):
    try:
        message = await webhook.send(content=content, avatar_url=str(member.display_avatar.url), files=attachments, wait=True)
        await message.add_reaction(pin_emoji)
    except:
        owner = await client.fetch_user(channel.guild.owner_id)
        await owner.send(f"`{channel.guild.name}`: Failed to send pinned message in the specified channel.\nLikely culprit: No Permission, File too large, File invalid")

def is_valid(client, info, message):
    if info.member.id == client.user.id:
        return False
    if guildprefs.get_guild_pref(message.guild.id, "pinboard") is False:
        return False
    return True

async def no_channel_error(client, guild):
    owner = await client.fetch_user(guild.owner_id)
    prefix = guildprefs.get_guild_pref(guild.id, "prefix")
    await owner.send(f"`{guild.name}`: Failed to send pinned message in the specified channel.\nLikely culprit: Channel Deleted\nAction needed: activate {prefix}userlog and enter a new channel ID")
    guildprefs.edit_guild_pref(guild.id, "userlog", False)
    guildprefs.edit_guild_pref(guild.id, "userlog_channel", 0)

async def get_channel_if_valid_from_member(client, member):
    guild = member.guild
    if guildprefs.get_guild_pref(guild.id, "pinboard"):
        channel_id = guildprefs.get_guild_pref(guild.id, "pinboard_channel")
        channel = guild.get_channel(int(channel_id))
        if channel is None:
            await no_channel_error(client, guild)
        return channel