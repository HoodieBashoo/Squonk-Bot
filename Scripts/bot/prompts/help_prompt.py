from prompts import helpinfo

class HelpPrompt():
    def __init__(self, author, guild, channel, timer, exit_func):
        self.author = author
        self.guild = guild
        self.channel = channel
        self.timer = timer
        self.exit_func = exit_func
        self.requested_responses = []
        self.state = 0
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
            case 0:
                self.requested_responses = ["all", "config", "utility"]
                self.state = 1
                await self.next_message("What commands are you looking for help with? (all/config/utility)")
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
                    await self.next_message("Not a category :( (all/config/utility)")

        if successful:
            print("Resetting timer")

        if message is not None:
            await message.delete()

    async def send_embeds(self, embeds):
        if self.previous_message is not None:
            await self.previous_message.delete()
        for embed in embeds:
            await self.channel.send(embed=embed)

    async def send_embed(self, embed):
        if self.previous_message is not None:
            await self.previous_message.delete()
        await self.channel.send(embed=embed)

    async def next_message(self, content):
        if self.interrupted is False and self.previous_message is not None:
            await self.previous_message.edit(content=content)
        elif self.interrupted is True and self.previous_message is not None:
            await self.previous_message.delete()
            self.previous_message = await self.channel.send(content)
        else:
            print("Setting first message as jimmy!")
            self.previous_message = await self.channel.send(content)

    async def cancel_prompt(self):
        self.stop_timer()
        await self.channel.send("Prompt cancelled")
        await self.exit_func(self.channel)

    async def close_prompt(self):
        self.stop_timer()
        await self.exit_func(self.channel)

    def stop_timer(self):
        print("Stopping timer")

    def interrupt(self):
        self.interrupted = True