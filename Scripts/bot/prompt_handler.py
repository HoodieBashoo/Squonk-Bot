from typing import NamedTuple

import prompts
from prompts.userlog_prompt import UserlogPrompt
from timer import Timer


active_prompts = []
#timers = {}

def reset():
    active_prompts = []

async def start_prompt(author, guild, channel, prompt_type, start_condition):
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

    new_timer = Timer(30, channel, end_prompt)
    #timers[channel.id] = new_timer
    new_prompt = await create_prompt(author, guild, channel, prompt_type, start_condition, end_prompt, new_timer)

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

async def process_satisfaction(message):
    channel_id = message.channel.id
    prompt = find_prompt(channel_id)
    await prompt.next_state(message.content)

async def end_prompt(channel):
    channel_id = channel.id
    prompt = find_prompt(channel_id)

    prompt.timer.stop_timer()
    active_prompts.remove(prompt)
    #timers[channel.id].stop_timer()
    #timers.pop(channel.id, None)
    await channel.send("Prompt ended")

def get_prompt_data(prompt_type, prompt, answer):
    match prompt_type:
        case "userlog":
            message, responses = userlog_prompt.get_prompt_data(prompt.prompt_state)
            return message, responses

async def create_prompt(author, guild, channel, prompt_type, start_condition, exit_func, timer):
    match prompt_type:
        case "userlog":
            prompt = UserlogPrompt(author, guild, channel, prompt_type, start_condition, exit_func, timer)
            timer.start_timer()
            active_prompts.append(prompt)
            await prompt.next_state("")

def debug_prompts():
    channel_id = 123123
    start_prompt(channel_id, "userlog")
    prompt = find_prompt(channel_id)
    prompt.exit_func(channel_id)

#debug_prompts()
