from prompts import helpinfo
from prompts.base_prompt import BasePrompt

class HelpPrompt(BasePrompt):
    def __init__(self, author, guild, channel, exit_func, cancel_emoji):
        BasePrompt.__init__(self, author, guild, channel, exit_func, cancel_emoji)

    async def next_state(self, message, response):
        if response == "cancel" or response == "stop" or response == "end":
            await self.cancel_prompt()
            return
        if response == "":
            print("Starting timer")

        current_state = self.state
        match current_state:
            case 0:
                self.requested_responses = ["all", "config", "utility"]
                self.state = 1
                await self.next_message("What commands are you looking for help with? (all/config/utility)", self.ResponseType.Normal)
            case 1:
                if response == self.requested_responses[0]:
                    embeds = helpinfo.all_embeds()
                    await self.send_embeds(embeds)
                    await self.close_prompt()
                elif response == self.requested_responses[1]:
                    embeds = helpinfo.config_embed()
                    await self.send_embed(embeds)
                    await self.close_prompt()
                elif response == self.requested_responses[2]:
                    embeds = helpinfo.utility_embed()
                    await self.send_embed(embeds)
                    await self.close_prompt()
                else:
                    await self.next_message("Not a category :( (all/config/utility)", self.ResponseType.Normal)

        if message is not None:
            await message.delete()
