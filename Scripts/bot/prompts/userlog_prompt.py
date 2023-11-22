from enum import Enum
import sys
sys.path.append("..")

import guildprefs

class UserlogPrompt():
    def __init__(self, author, guild, channel, timer, start_condition, exit_func, cancel_emoji):
        self.author = author
        self.guild = guild
        self.channel = channel
        self.timer = timer
        self.exit_func = exit_func
        self.cancel_emoji = cancel_emoji
        self.requested_responses = []
        if (start_condition == "enabled"):
            self.state = 10
        elif (start_condition == "disabled"):
            self.state = 0
        self.final_prefs = {
            "userlog": False,
            "userlog_channel": 0
        }
        self.interrupted = False
        self.previous_message = None

    async def next_state(self, message, response):
        if response == "cancel" or response == "stop" or response == "end":
            await self.cancel_prompt()
            return
        if response == "":
            print("Starting timer")

        successful = False
        currentState = self.state
        match currentState:
            # PURPOSE: USERLOG NOT YET ENABLED
            case 0:
                self.requested_responses = ["y", "n"]
                self.state = 1
                await self.next_message("Would you like to enable userlog? (y/n)", self.ResponseType.Normal)
            case 1:
                if response == self.requested_responses[0]:
                    self.requested_responses = []
                    self.state = 2
                    await self.next_message("Send the ID for the channel you wish to use", self.ResponseType.Normal)
                    successful = True
                elif response == self.requested_responses[1]:
                    await self.cancel_prompt()
            case 2:
                if response.isdigit():
                    if self.guild.get_channel(int(response)) is not None:
                        self.final_prefs["userlog"] = True
                        self.final_prefs["userlog_channel"] = response
                        guildprefs.edit_guild_pref(self.guild.id, "userlog", self.final_prefs["userlog"])
                        guildprefs.edit_guild_pref(self.guild.id, "userlog_channel", self.final_prefs["userlog_channel"])
                        await self.next_message("Successfully set userlog channel", self.ResponseType.End)
                        await self.close_prompt()
                    else:
                        await self.next_message("Couldn't find a channel with that ID", self.ResponseType.Normal)
                        successful = True
                else:
                    await self.next_message("Not an ID! Please send a channel ID", self.ResponseType.Normal)

            # PURPOSE: USERLOG ALREADY ENABLED
            case 10:
                self.requested_responses = ["change", "disable"]
                self.state = 11
                await self.next_message("Would you like to change or disable the log channel? (change/disable)", self.ResponseType.Normal)
            case 11:
                if response == self.requested_responses[0]:
                    self.requested_responses = []
                    self.state = 2
                    await self.next_message("Oke, send a new channel ID", self.ResponseType.Normal)
                    successful = True
                elif response == self.requested_responses[1]:
                    self.final_prefs["userlog"] = False
                    self.final_prefs["userlog_channel"] = 0
                    guildprefs.edit_guild_pref(self.guild.id, "userlog", self.final_prefs["userlog"])
                    guildprefs.edit_guild_pref(self.guild.id, "userlog_channel", self.final_prefs["userlog_channel"])
                    await self.next_message("Successfully disabled userlog", self.ResponseType.End)
                    await self.close_prompt()

        if successful:
            self.interrupted = False
            print("Resetting timer")

        if message is not None:
            await message.delete()

    async def next_message(self, content, response_type):
        if self.interrupted is False and self.previous_message is not None:
            await self.previous_message.edit(content=content)
            await self.previous_message.clear_reactions()
            await self.add_cancel_emoji(response_type)
        elif self.interrupted is True and self.previous_message is not None:
            await self.previous_message.delete()
            self.previous_message = await self.channel.send(content)
            await self.add_cancel_emoji(response_type)
        else:
            self.previous_message = await self.channel.send(content)
            await self.add_cancel_emoji(response_type)

    async def add_cancel_emoji(self, response_type):
        if response_type is not self.ResponseType.End:
            await self.previous_message.add_reaction(self.cancel_emoji)

    async def cancel_prompt(self):
        await self.channel.send("Prompt cancelled")
        await self.exit_func(self.channel)

    async def close_prompt(self):
        print("Stopping timer")
        await self.exit_func(self.channel)

    def interrupt(self):
        # yeah it just sets every time, it's chill! Whatever!
        self.interrupted = True

    class ResponseType(Enum):
        Normal = 1,
        End = 2