from prompts import *

active_prompts = []
prompt_time = 5
cancel_emoji = "❌"

# TODO: Add a timer so that prompts end after 30 seconds of inactivity

async def start_prompt(client, author, guild, channel, prompt_type, start_condition):
    if find_prompt(channel.id) is not None:
        await channel.send("Another prompt is already running in this channel")
        return

    guild_prompts = find_prompts(guild.id)
    if guild_prompts is not None:
        if len(guild_prompts) > 0:
            for prompt in guild_prompts:
                if prompt.prompt_type == prompt_type:
                    await channel.send(f"A {prompt_type} prompt is already running in this server")
                    return

    await create_prompt(client, author, guild, channel, prompt_type, start_condition, end_prompt)

def find_prompt(channel_id):
    if len(active_prompts) <= 0:
        return

    for prompt in active_prompts:
        if prompt.channel.id == channel_id:
            return prompt

def find_prompts(guild_id):
    if len(active_prompts) <= 0:
        return

    guild_prompts = []
    for prompt in active_prompts:
        if prompt.guild.id == guild_id:
            guild_prompts.append(prompt)
    return guild_prompts

async def process_satisfaction(prompt, message):
    if prompt.author == message.author:
        await prompt.next_state(message, message.content.lower())
    else:
        prompt.interrupt()

async def reaction_cancel(prompt, user):
    if prompt.author == user:
        await prompt.cancel_prompt()

async def end_prompt(channel):
    channel_id = channel.id
    prompt = find_prompt(channel_id)
    active_prompts.remove(prompt)

async def create_prompt(client, author, guild, channel, prompt_type, start_condition, exit_func):
    prompt = None

    match prompt_type:
        case "userlog":
            prompt = UserlogPrompt(author, guild, channel, start_condition, exit_func, cancel_emoji)
        case "help":
            prompt = HelpPrompt(author, guild, channel, exit_func, cancel_emoji)
        case "pinboard":
            prompt = PinboardPrompt(client, author, guild, channel, start_condition, exit_func, cancel_emoji)
        case "twithelper":
            prompt = TwitterPrompt(author, guild, channel, start_condition, exit_func, cancel_emoji)

    if prompt is not None:
        active_prompts.append(prompt)
        await prompt.next_state(None, "")
    else:
        await channel.send("Error creating prompt")
