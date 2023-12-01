from enum import Enum

class BasePrompt:
    def __init__(self, author, guild, channel, exit_func, cancel_emoji):
        self.author = author
        self.guild = guild
        self.channel = channel
        self.exit_func = exit_func
        self.cancel_emoji = cancel_emoji
        self.requested_responses = []
        self.state = 0
        self.interrupted = False
        self.previous_message = None

    async def next_state(self, message, response):
        # TODO: Clean this up so that there isn't any duplicate code across the prompts, since this entire method needs to be overwritten
        print("Unimplemented next_state")

        if response == "cancel" or response == "stop" or response == "end":
            await self.cancel_prompt()
            return
        if response == "":
            print("Starting timer")
        
        successful = False
        current_state = self.state

        match current_state:
            case "example":
                pass

        if successful:
            print("Resetting timer")

        if message is not None:
            # TODO: Add a try except here for no permissions
            await message.delete()

    async def send_embeds(self, embeds):
        if self.previous_message is not None:
            await self.previous_message.delete()
        await self.channel.send(embeds=embeds)

    async def send_embed(self, embed):
        if self.previous_message is not None:
            await self.previous_message.delete()
        await self.channel.send(embed=embed)

    async def next_message(self, content, response_type):
        if self.interrupted is False and self.previous_message is not None:
            await self.previous_message.edit(content=content)
            if response_type is self.ResponseType.End:
                await self.previous_message.clear_reactions()
        elif self.interrupted is True and self.previous_message is not None:
            await self.previous_message.delete()
            self.previous_message = await self.channel.send(content)
            await self.add_cancel_emoji(response_type)
            self.interrupted = False
        else:
            self.previous_message = await self.channel.send(content)
            await self.add_cancel_emoji(response_type)

    async def add_cancel_emoji(self, response_type):
        if response_type is not self.ResponseType.End:
            await self.previous_message.add_reaction(self.cancel_emoji)

    async def cancel_prompt(self):
        self.stop_timer()
        await self.next_message("Prompt cancelled", self.ResponseType.End)
        await self.exit_func(self.channel)

    async def close_prompt(self):
        self.stop_timer()
        await self.exit_func(self.channel)

    def stop_timer(self):
        print("Stopping timer")

    def interrupt(self):
        self.interrupted = True

    class ResponseType(Enum):
        Normal = 1,
        End = 2
