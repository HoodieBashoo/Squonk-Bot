import sys
sys.path.append("..")

import guildprefs
from prompts.base_prompt import BasePrompt

class TwitterPrompt(BasePrompt):
    def __init__(self, author, guild, channel, start_condition, exit_func, cancel_emoji):
        BasePrompt.__init__(self, author, guild, channel, exit_func, cancel_emoji)
        if start_condition == "enabled":
            self.state = 10
        elif start_condition == "disabled":
            self.state = 0
        self.final_prefs = {
            "twithelper": False,
            "twitter_button_time": 0
        }

    async def next_state(self, message, response):
        if response == "cancel" or response == "stop" or response == "end":
            await self.cancel_prompt()
            return
        if response == "":
            print("Starting timer")

        current_state = self.state
        match current_state:
            # TWITHELPER NOT ENABLED YET
            case 0:
                self.requested_responses = ["y", "n"]
                self.state = 1
                await self.next_message("Would you like to enable the twitter helper? (y/n)", self.ResponseType.Normal)
            case 1:
                if response == self.requested_responses[0]:
                    self.final_prefs["twithelper"] = True
                    self.requested_responses = []
                    self.state = 2
                    await self.next_message("How many seconds would you like the helper buttons to stick around for?", self.ResponseType.Normal)
                elif response == self.requested_responses[1]:
                    await self.cancel_prompt()
            case 2:
                if response.isdigit():
                    guildprefs.edit_guild_pref(self.guild.id, "twithelper", self.final_prefs["twithelper"])
                    guildprefs.edit_guild_pref(self.guild.id, "twitter_button_time", int(response))
                    await self.next_message("Successfully enabled the twitter helper!", self.ResponseType.End)
                    await self.close_prompt()
                else:
                    await self.next_message("Not a number! Please send a number of seconds for the helper buttons", self.ResponseType.Normal)

            # TWITHELPER ENABLED ALREADY
            case 10:
                self.requested_responses = ["change", "disable"]
                self.state = 11
                await self.next_message("Do you wanna change or disable the twitter helper? (change/disable)", self.ResponseType.Normal)
            case 11:
                if response == self.requested_responses[0]:
                    self.requested_responses = []
                    self.state = 12
                    await self.next_message("How long would you like the helper buttons to stick around for?", self.ResponseType.Normal)
                elif response == self.requested_responses[1]:
                    guildprefs.edit_guild_pref(self.guild.id, "twithelper", False)
                    guildprefs.edit_guild_pref(self.guild.id, "twitter_button_time", 0)
                    await self.next_message("Successfully disabled the twitter helper", self.ResponseType.End)
                    await self.close_prompt()
            case 12:
                if response.isdigit():
                    guildprefs.edit_guild_pref(self.guild.id, "twitter_button_time", int(response))
                    await self.next_message("Successfully changed button time", self.ResponseType.End)
                    await self.close_prompt()
                else:
                    await self.next_message("Not a number! Please send a number of seconds for the helper buttons", self.ResponseType.Normal)

        if message is not None:
            await message.delete()