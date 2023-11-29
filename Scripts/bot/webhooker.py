import discord

import guildprefs

default_name = "Squonk Webhook"

async def get_webhook(client, channel):
    webhooks = await channel.webhooks()
    sending_webhook = None

    if webhooks:
        for webhook in webhooks:
            if webhook.user.id == client.user.id:
                sending_webhook = webhook
                break

    if sending_webhook is None:
        try:
            sending_webhook = await channel.create_webhook(name=default_name)
        except:
            owner = await client.fetch_user(channel.guild.owner_id)
            await owner.send(
                f"`{channel.guild.name}`: Failed to create webhook in {channel.name}.\nLikely culprits: No Permission")

    return sending_webhook

async def send_webhook(client, channel, content, **kwargs):
    name = kwargs.get("name", str)
    avatar_url = kwargs.get("avatar_url", str)
    files = kwargs.get("files", None)
    embeds = kwargs.get("embeds", None)
    wait = kwargs.get("wait", bool)
    reaction = kwargs.get("reaction", None)
    view = kwargs.get("view", None)

    webhook = await get_webhook(client, channel)
    if webhook is None:
        return

    if embeds or files is None:
        files = ()
        embeds = ()
    message = await webhook.send(content=content, username=name, avatar_url=avatar_url, files=files, embeds=embeds, wait=wait)

    if reaction is not None:
        await message.add_reaction(reaction)
    if view is not None and wait is True:
        await message.edit(view=view)
        view.set_helper_message(message)
    return message

async def send_webhook_as_user(client, channel, content, member, **kwargs):
    files = kwargs.get("files", None)
    embeds = kwargs.get("embeds", None)
    wait = kwargs.get("wait", bool)
    reaction = kwargs.get("reaction", None)
    view = kwargs.get("view", None)

    await send_webhook(client, channel, content, name=get_name(member), avatar_url=str(member.display_avatar.url), files=files, embeds=embeds, reaction=reaction, wait=wait, view=view)

def get_name(member):
    name = None
    if (member.global_name is not None):
        name = member.global_name
    else:
        name = member.name
    return name