import guildprefs

async def member_joined(member):
    channel = get_channel_if_valid_from_member(member)
    if channel is not None:
        # TODO: Add random welcome message after the period
        await channel.send(f"{member.mention} has entered the chat.")

async def member_left(member):
    # TODO: Check if the user was kicked instead of left
    channel = get_channel_if_valid_from_member(member)
    if channel is not None:
        # TODO: Add random hate message after the period
        await channel.send(f"{member.name} has left the chat.")

async def member_banned(guild, member):
    channel = get_channel_if_valid_from_guild(guild)
    if channel is not None:
        await channel.send(f"{member.name} has been banned.")

async def member_unbanned(guild, member):
    channel = get_channel_if_valid_from_guild(guild)
    if channel is not None:
        await channel.send(f"{member.name} has been unbanned.")

def get_channel_if_valid_from_guild(guild):
    if guildprefs.get_guild_pref(guild.id, "userlog"):
        channel_id = guildprefs.get_guild_pref(guild.id, "userlog_channel")
        channel = guild.get_channel(int(channel_id))
        return channel

def get_channel_if_valid_from_member(member):
    guild = member.guild
    if guildprefs.get_guild_pref(guild.id, "userlog"):
        channel_id = guildprefs.get_guild_pref(guild.id, "userlog_channel")
        channel = guild.get_channel(int(channel_id))
        return channel