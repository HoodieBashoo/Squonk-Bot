import discord
from discord.ui import Button, View

async def send_helper(message, twitter_links):
    # collect all links in message
    # slice each to just be the website name, and if the website name is x or twitter, add the link to a list
    # send this message with all twitter links
    content = ""
    for link in twitter_links:
        content += f" {link}"

    await message.channel.send(content, view=twitter_buttons(message))
    # depending on button pressed, edit each link with the specified jimmy
    pass

def get_twitter_links(content):
    https_indices = []
    search_index = 0
    while True:
        instance = content.find("https", search_index)
        if instance >= 0:
            search_index = instance + 1
            https_indices.append(instance)
        else:
            break

    if https_indices:
        links = []
        for index in https_indices:
            if content.find("www", index, index + 11) >= 0:
                x = content[slice(index + 12, index + 13)]
                twitter = content[slice(index + 12, index + 19)]
            else:
                x = content[slice(index + 8, index + 9)]
                twitter = content[slice(index + 8, index + 15)]
            if x == "x" or twitter == "twitter":
                final_index = content.find(" ", index)
                if final_index >= 0:
                    link = content[slice(index, content.find(" ", index))]
                    links.append(link)
                else:
                    link = content[index:]
                    links.append(link)

        print(f"Twitter links: {links}")
        return links
    else:
        return False

async def edit_helper_message(message, replacement):
    content = message.content
    search_terms = ["fxtwitter", "vxtwitter", "fixupx", "x", "twitter"]
    for term in search_terms:
        index = content.find(term)
        if index >= 0:
            print(f"{content[index]} {content[index + 1]}")
            print(f"{content[index]} {content[index - 1]}")
            if term == "x":
                if content[index + 1] != "t" or content[index - 1] != "p":
                    print(f"replacing {term} with {replacement}")
                    content = content.replace(term, replacement)
            else:
                content = content.replace(term, replacement)
    await message.edit(content=content)

class twitter_buttons(View):
    def __init__(self, message):
        self.message = message
        View.__init__(self, timeout=30)

    @discord.ui.button(label="vx", style=discord.ButtonStyle.secondary)
    async def vx_callback(self, interaction, button):
        await edit_helper_message(interaction.message, "vxtwitter")
        await self.message.channel.send("vx")
        await interaction.response.defer()

    @discord.ui.button(label="fx", style=discord.ButtonStyle.secondary)
    async def fx_callback(self, interaction, button):
        await edit_helper_message(interaction.message, "fxtwitter")
        await self.message.channel.send("fx")
        await interaction.response.defer()

    @discord.ui.button(label="fixupx", style=discord.ButtonStyle.secondary)
    async def fixupx_callback(self, interaction, button):
        await edit_helper_message(interaction.message, "fixupx")
        await self.message.channel.send("fixupx")
        await interaction.response.defer()

    @discord.ui.button(label="direct", style=discord.ButtonStyle.secondary)
    async def direct_callback(self, interaction, button):
        await edit_helper_message(interaction.message, "twitter")
        await self.message.channel.send("direct")
        await interaction.response.defer()