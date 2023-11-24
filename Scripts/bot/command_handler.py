import test
import time

import botinfo
import commands


def on_start(time):
    commands.utility.on_start(time)

async def process_command(client, message, prefix):
    content = message.content
    # TODO: Find the space after the last space in the prefix if it has one
    next_space_index = content.find(" ")
    if (next_space_index < 0):
        command = content[len(prefix):]
        parameter = ""
    else:
        command = content[len(prefix):next_space_index]
        parameter = content[next_space_index+1:]

    await run_command(client, message, command, parameter)
    pass

async def run_command(client, message, command, parameter):
    await config_commands(client, message, command, parameter)
    await utility_commands(client, message, command, parameter)

async def utility_commands(client, message, command, parameter):
    match command:
        case "shutdown":
            await commands.utility.shutdown(client, message)
        case "help":
            await commands.utility.help(client, message, parameter)
        case "update":
            await commands.utility.update(client, message)
        case "ping":
            await commands.utility.ping(client, message)
        case "info":
            await commands.utility.info(message)
        case "updateprefs":
            await commands.utility.prefs_update(client, message)

async def config_commands(client, message, command, parameter):
    # TODO: Add a permission system for specific commands,
    #  config commands are manually disabled for other users rn
    match command:
        case "prefix":
            await commands.config.update_prefix(message, parameter, message.channel)
        case "updateprefix":
            await commands.config.update_prefix(message, parameter, message.channel)
        case "userlog":
            await commands.config.userlog(client, message)
        case "pinboard":
            await commands.config.pinboard(client, message)
        case "twithelper":
            await commands.config.twitter_helper(message)