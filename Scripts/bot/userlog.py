import guildprefs

async def member_joined(client, member):
    channel = await get_channel_if_valid_from_member(client, member)
    if channel is not None:
        # TODO: Add random welcome message after the period
        await send_message(client, channel, f"{member.mention} has entered the chat.")

async def member_left(client, member):
    # TODO: Check if the user was kicked instead of left
    channel = await get_channel_if_valid_from_member(client, member)
    if channel is not None:
        # TODO: Add random hate message after the period
        await send_message(client, channel, f"{get_member_identification(member)} has left the chat.")

async def member_banned(client, guild, member):
    channel = await get_channel_if_valid_from_guild(client, guild)
    if channel is not None:
        await send_message(client, channel, f"{get_member_identification(member)} has been banned.")

async def member_unbanned(client, guild, member):
    channel = await get_channel_if_valid_from_guild(client, guild)
    if channel is not None:
        await send_message(client, channel, f"{get_member_identification(member)} has been unbanned.")

async def send_message(client, channel, content):
    try:
        await channel.send(content)
    except:
        owner = await client.fetch_user(channel.guild.owner_id)
        await owner.send(f"`{channel.guild.name}`: Failed to send userlog message in the specified channel.\nLikely culprit: No Permission")

async def no_channel_error(client, guild):
    owner = await client.fetch_user(guild.owner_id)
    prefix = guildprefs.get_guild_pref(guild.id, "prefix")
    await owner.send(f"`{guild.name}`: Failed to send userlog message in the specified channel.\nLikely culprit: Channel Deleted\nAction needed: activate {prefix}userlog and enter a new channel ID")
    guildprefs.edit_guild_pref(guild.id, "userlog", False)
    guildprefs.edit_guild_pref(guild.id, "userlog_channel", 0)

async def get_channel_if_valid_from_guild(client, guild):
    if guildprefs.get_guild_pref(guild.id, "userlog"):
        channel_id = guildprefs.get_guild_pref(guild.id, "userlog_channel")
        channel = guild.get_channel(int(channel_id))
        if channel is None:
            await no_channel_error(client, guild)
        return channel

async def get_channel_if_valid_from_member(client, member):
    guild = member.guild
    if guildprefs.get_guild_pref(guild.id, "userlog"):
        channel_id = guildprefs.get_guild_pref(guild.id, "userlog_channel")
        channel = guild.get_channel(int(channel_id))
        if channel is None:
            await no_channel_error(client, guild)
        return channel

def get_member_identification(member):
    if member.name == member.global_name.lower():
        return f"{member.name}"
    else:
        return f"{member.name} ({member.global_name})"