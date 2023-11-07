import botinfo


async def send_message(content, channel):
    await channel.send(content)

async def update_channel(message, input):
    if input.isdigit():
        channel = message.guild.get_channel(int(input))
        if channel is not None:
            botinfo.channel_id = channel.id
            await send_message(f"Channel updated to {channel.name}", message.channel)
    else:
        await send_message("Not a valid channel ID", message.channel)
