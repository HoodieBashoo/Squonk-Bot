import test
import botinfo
import commands

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
    #await test_commands(client, message, command, parameter)
    await config_commands(client, message, command, parameter)
    await utility_commands(client, message, command, parameter)

async def utility_commands(client, message, command, parameter):
    match command:
        case "shutdown":
            await commands.utility.shutdown(client, message)

async def config_commands(client, message, command, parameter):
    # TODO: Add a permission system for specific commands,
    #  config commands are manually disabled for other users rn
    match command:
        case "updateprefix":
            await commands.config.update_prefix(message, parameter, message.channel)
        case "userlog":
            await commands.config.userlog(message)

async def test_commands(client, message, command, parameter):
    match command:
        case "sendmessage":
            await test.send_message(parameter, message.guild.get_channel(botinfo.channel_id))
        case "updatechannel":
            await test.update_channel(message, parameter)