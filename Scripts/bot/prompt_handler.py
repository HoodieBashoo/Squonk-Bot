from typing import NamedTuple

from prompts import *
#from prompts.userlog_prompt import UserlogPrompt
#from prompts.help_prompt import HelpPrompt
from timer import Timer

active_prompts = []
prompt_time = 5

def reset():
    active_prompts = []

# TODO: Add a timer so that prompts end after 30 seconds of inactivity

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

    new_prompt = await create_prompt(author, guild, channel, prompt_type, start_condition, end_prompt)

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

async def end_prompt(channel):
    channel_id = channel.id
    prompt = find_prompt(channel_id)

    active_prompts.remove(prompt)
    #await channel.send("Prompt ended")

def get_prompt_data(prompt_type, prompt, answer):
    match prompt_type:
        case "userlog":
            message, responses = userlog_prompt.get_prompt_data(prompt.prompt_state)
            return message, responses

async def create_prompt(author, guild, channel, prompt_type, start_condition, exit_func):
    timer = Timer(prompt_time, channel, exit_func)
    prompt = None

    match prompt_type:
        case "userlog":
            prompt = UserlogPrompt(author, guild, channel, timer, start_condition, exit_func)
        case "help":
            prompt = HelpPrompt(author, guild, channel, timer, exit_func)

    if prompt is not None:
        active_prompts.append(prompt)
        await prompt.next_state(None, "")
    else:
        await channel.send("Error creating prompt")