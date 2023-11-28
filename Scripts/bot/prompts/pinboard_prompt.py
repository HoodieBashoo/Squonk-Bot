import emoji

import guildprefs
from prompts.base_prompt import BasePrompt


class PinboardPrompt(BasePrompt):
    def __init__(self, client, author, guild, channel, timer, start_condition, exit_func, cancel_emoji):
        BasePrompt.__init__(self, author, guild, channel, timer, exit_func, cancel_emoji)
        self.client = client
        if (start_condition == "enabled"):
            self.state = 10
        elif (start_condition == "disabled"):
            self.state = 0
        self.final_prefs = {
            "pinboard": False,
            "pinboard_channel": 0,
            "pin_activation_emoji": ""
        }

    async def next_state(self, message, response):
        if response == "cancel" or response == "stop" or response == "end":
            await self.cancel_prompt()
            return
        if response == "":
            print("Starting timer")

        successful = False
        currentState = self.state
        match currentState:
            # PURPOSE: Pinboard NOT YET ENABLED
            case 0:
                self.requested_responses = ["y", "n"]
                self.state = 1
                await self.next_message("Would you like to enable pinboard? (y/n)", self.ResponseType.Normal)
            case 1:
                if response == self.requested_responses[0]:
                    self.requested_responses = []
                    self.state = 2
                    await self.next_message("Send the ID of the channel you want to pin messages to", self.ResponseType.Normal)
                    successful = True
                elif response == self.requested_responses[1]:
                    await self.cancel_prompt()
            case 2:
                if response.isdigit():
                    if self.guild.get_channel(int(response)) is not None:
                        self.final_prefs["pinboard"] = True
                        self.final_prefs["pinboard_channel"] = response
                        self.state = 3
                        self.requested_responses = []
                        await self.next_message("And what emoji do you want to use to pin messages?", self.ResponseType.Normal)
                        successful = True
                    else:
                        await self.next_message("Couldn't find a channel with that ID", self.ResponseType.Normal)
                        successful = True
                else:
                    await self.next_message("Not an ID! Please send a channel ID", self.ResponseType.Normal)
            case 3:
                print(response)
                emoji_id = response.split(":", 2)[-1][:-1]
                try:
                    emoji_object = self.client.get_emoji(int(emoji_id))
                    print(f"Got emoji: {emoji_object}")
                    if emoji_object is not None:
                        self.final_prefs["pin_activation_emoji"] = emoji_id
                        self.set_prefs()
                        await self.next_message(f"Successfully configured pinboard channel with emoji: {self.client.get_emoji(int(emoji_id))}", self.ResponseType.End)
                        await self.close_prompt()
                    else:
                        await self.next_message("Err I don't think I know that emoji", self.ResponseType.Normal)
                except:
                    if emoji.is_emoji(response):
                        self.final_prefs["pin_activation_emoji"] = response
                        self.set_prefs()
                        await self.next_message(f"Successfully configured pinboard channel with emoji: {response}", self.ResponseType.End)
                        await self.close_prompt()
                    else:
                        await self.next_message("Invalid response, please only include the emoji in your response", self.ResponseType.Normal)

            # PURPOSE: PINBOARD ALREADY ENABLED
            case 10:
                self.requested_responses = ["change", "disable"]
                self.state = 11
                await self.next_message("Would you like to change or disable the pinboard channel? (change/disable)", self.ResponseType.Normal)
            case 11:
                if response == self.requested_responses[0]:
                    self.requested_responses = []
                    self.state = 2
                    await self.next_message("Righty then, send a new channel ID", self.ResponseType.Normal)
                    successful = True
                elif response == self.requested_responses[1]:
                    self.final_prefs["pinboard"] = False
                    self.final_prefs["pinboard_channel"] = 0
                    guildprefs.edit_guild_pref(self.guild.id, "pinboard", self.final_prefs["pinboard"])
                    guildprefs.edit_guild_pref(self.guild.id, "pinboard_channel", self.final_prefs["pinboard_channel"])
                    await self.next_message("Successfully disabled pinboard", self.ResponseType.End)
                    await self.close_prompt()

        if successful:
            print("Resetting timer")

        if message is not None:
            await message.delete()

    def detect_emoji(self, text):
        for emoji in UNICODE_EMOJI:
            if text == emoji:
                return True
        return False

    def set_prefs(self):
        guildprefs.edit_guild_pref(self.guild.id, "pinboard", self.final_prefs["pinboard"])
        guildprefs.edit_guild_pref(self.guild.id, "pinboard_channel", self.final_prefs["pinboard_channel"])
        guildprefs.edit_guild_pref(self.guild.id, "pin_activation_emoji", self.final_prefs["pin_activation_emoji"])