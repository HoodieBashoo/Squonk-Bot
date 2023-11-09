import sys
sys.path.append("..")

import botinfo


async def shutdown(client, message):
    if message.author.id == botinfo.owner_id:
        await message.channel.send("Shutting down...")
        await client.close()
    else:
        await message.channel.send("You do not have permission to do this")