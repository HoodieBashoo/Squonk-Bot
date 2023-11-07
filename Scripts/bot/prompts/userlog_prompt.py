class UserlogPrompt():
    def __init__(self, author, guild, channel, prompt_type, start_condition, exit_func):
        self.author = author
        self.guild = guild
        self.channel = channel
        self.prompt_type = prompt_type
        self.timer_length = 5
        self.exit_func = exit_func
        self.requested_responses = []
        if (start_condition == "enabled"):
            self.state = 10
        elif (start_condition == "disabled"):
            self.state = 0

    async def next_state(self, response):
        if response == "cancel":
            await self.close_prompt()
        if response == "":
            print("Starting timer")

        successful = False
        currentState = self.state
        match currentState:
            # PURPOSE: USERLOG NOT YET ENABLED
            case 0:
                self.requested_responses = ["y", "n"]
                self.state = 1
                await self.channel.send("Would you like to enable userlog? (y/n)")
            case 1:
                if response == self.requested_responses[0]:
                    self.requested_responses = []
                    self.state = 2
                    await self.channel.send("gtfo in here with a channel ID jimmy")
                    successful = True
                elif response == self.requested_responses[1]:
                    await self.close_prompt()
            case 2:
                pass

            # PURPOSE: USERLOG ALREADY ENABLED
            case 10:
                self.requested_responses = ["change", "disable"]
                self.state = 11
                await self.channel.send("Would you like to change or disable the log channel? (change/disable)")
            case 11:
                if response == self.requested_responses[0]:
                    self.requested_responses = []
                    self.state = 2
                    await self.channel.send("gtfih with a new channel ID jimmy")
                    successful = True
                elif response == self.requested_responses[1]:
                    #guildprefs log_channel: 0
                    #guildprefs userlog: False
                    await self.close_prompt()

        if successful:
            print("Resetting timer")

    async def close_prompt(self):
        print("Stopping timer")
        await self.exit_func(self.channel)
