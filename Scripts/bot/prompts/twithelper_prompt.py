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

    async def next_state(self, message, response):
        if response == "cancel" or response == "stop" or response == "end":
            await self.cancel_prompt()
            return
        if response == "":
            print("Starting timer")

        successful = False
        current_state = self.state

        match current_state:
            case 0:
                self.requested_responses = ["y", "n"]
                self.state = 1
                await self.next_message("Would you like to enable the twitter helper? (y/n)", self.ResponseType.Normal)
            case 1:
                if response == self.requested_responses[0]:
                    guildprefs.edit_guild_pref(self.guild.id, "twithelper", True)
                    await self.next_message("Successfully enabled the twitter helper", self.ResponseType.End)
                    await self.close_prompt()
                elif response == self.requested_responses[1]:
                    await self.cancel_prompt()

            case 10:
                self.requested_responses = ["y", "n"]
                self.state = 11
                await self.next_message("Do you wanna disable the twitter helper? (y/n)", self.ResponseType.Normal)
            case 11:
                if response == self.requested_responses[0]:
                    guildprefs.edit_guild_pref(self.guild.id, "twithelper", False)
                    await self.next_message("Successfully disabled the twitter helper", self.ResponseType.End)
                    await self.close_prompt()
                elif response == self.requested_responses[1]:
                    await self.cancel_prompt()

        if successful:
            print("Resetting timer")

        if message is not None:
            await message.delete()
