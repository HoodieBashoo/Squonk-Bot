import discord
from discord.ui import Button, View

async def send_helper(message):
    # collect all links in message
    # slice each to just be the website name, and if the website name is x or twitter, add the link to a list
    # send this message with all twitter links
    await message.channel.send("Example", view=twitter_buttons(message))
    # depending on button pressed, edit each link with the specified jimmy

def has_twitter_link(message):
    # find first instance of https
    # slice the string to just be the website name
    # if website name is x or twitter, return True
    # else return False
    pass

class twitter_buttons(View):
    def __init__(self, message):
        self.message = message
        View.__init__(self, timeout=30)

    @discord.ui.button(label="vx", style=discord.ButtonStyle.secondary)
    async def vx_callback(self, interaction, button):
        await self.message.channel.send("vx")
        await interaction.response.defer()

    @discord.ui.button(label="fx", style=discord.ButtonStyle.secondary)
    async def fx_callback(self, interaction, button):
        await self.message.channel.send("fx")
        await interaction.response.defer()

    @discord.ui.button(label="fixupx", style=discord.ButtonStyle.secondary)
    async def fixupx_callback(self, interaction, button):
        await self.message.channel.send("fixupx")
        await interaction.response.defer()

    @discord.ui.button(label="direct", style=discord.ButtonStyle.secondary)
    async def direct_callback(self, interaction, button):
        await self.message.channel.send("direct")
        await interaction.response.defer()
