import test
import botinfo


async def process_command(message):
    content = message.content
    next_space_index = content.find(" ")
    if (next_space_index < 0):
        return
    command = content[len(botinfo.prefix):next_space_index]
    parameter = content[next_space_index+1:]
    #print(f"command: {command}")
    #print(f"input: {input}")
    await run_command(message, command, parameter)
    pass

async def run_command(message, command, parameter):
    match command:
        case "sendmessage":
            await test.send_message(parameter, message.guild.get_channel(botinfo.channel_id))
        case "updatechannel":
            await test.update_channel(message, parameter)