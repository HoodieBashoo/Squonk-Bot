import test
import botinfo
import commands

async def process_command(message, prefix):
    content = message.content
    # TODO: Find the space after the last space in the prefix if it has one
    next_space_index = content.find(" ")
    if (next_space_index < 0):
        command = content[len(prefix):]
        parameter = ""
    else:
        command = content[len(prefix):next_space_index]
        parameter = content[next_space_index+1:]

    #await message.channel.send(f"command received: {command} with parameter: {parameter}")
    await run_command(message, command, parameter)
    pass

async def run_command(message, command, parameter):
    await test_commands(message, command, parameter)
    await config_commands(message, command, parameter)

async def config_commands(message, command, parameter):
    match command:
        case "updateprefix":
            await commands.config.update_prefix(message.guild.id, parameter, message.channel)
        case "userlog":
            await commands.config.userlog(message)

async def test_commands(message, command, parameter):
    match command:
        case "sendmessage":
            await test.send_message(parameter, message.guild.get_channel(botinfo.channel_id))
        case "updatechannel":
            await test.update_channel(message, parameter)