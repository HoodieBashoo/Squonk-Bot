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

    async def next_state(self, response):
        if response == "cancel":
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
                await self.channel.send("What commands are you looking for help with? (all/config/utility)")
            case 1:
                if response == self.requested_responses[0]:
                    embeds = helpinfo.all_embeds()
                    for embed in embeds:
                        await self.channel.send(embed=embed)
                    await self.close_prompt()
                if response == self.requested_responses[1]:
                    await self.channel.send(embed=helpinfo.config_embed())
                    await self.close_prompt()
                if response == self.requested_responses[2]:
                    await self.channel.send(embed=helpinfo.utility_embed())
                    await self.close_prompt()

        if successful:
            print("Resetting timer")

    async def cancel_prompt(self):
        self.stop_timer()
        await self.channel.send("Prompt cancelled")
        await self.exit_func(self.channel)

    async def close_prompt(self):
        self.stop_timer()
        await self.exit_func(self.channel)

    def stop_timer(self):
        print("Stopping timer")

