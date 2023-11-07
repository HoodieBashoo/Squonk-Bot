from typing import NamedTuple

import prompts
from prompts.userlog_prompt import UserlogPrompt


active_prompts = []

async def start_prompt(author, guild, channel, prompt_type, start_condition):
    new_prompt = await create_prompt(author, guild, channel, prompt_type, start_condition, end_prompt)

def find_prompt(channel_id):
    if len(active_prompts) <= 0:
        return

    for prompt in active_prompts:
        if prompt.channel.id == channel_id:
            return prompt

async def process_satisfaction(message):
    channel_id = message.channel.id
    prompt = find_prompt(channel_id)
    await prompt.next_state(message.content)

async def end_prompt(channel):
    channel_id = channel.id
    prompt = find_prompt(channel_id)
    active_prompts.remove(prompt)
    await channel.send("Prompt ended")

def get_prompt_data(prompt_type, prompt, answer):
    match prompt_type:
        case "userlog":
            message, responses = userlog_prompt.get_prompt_data(prompt.prompt_state)
            return message, responses

async def create_prompt(author, guild, channel, prompt_type, start_condition, exit_func):
    match prompt_type:
        case "userlog":
            prompt = UserlogPrompt(author, guild, channel, start_condition, exit_func)
            active_prompts.append(prompt)
            await prompt.next_state("")

def debug_prompts():
    channel_id = 123123
    start_prompt(channel_id, "userlog")
    prompt = find_prompt(channel_id)
    prompt.exit_func(channel_id)

#debug_prompts()
