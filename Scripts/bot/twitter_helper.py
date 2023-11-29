import discord
from discord.ui import Button, View

button_time = 30
default_edit = "fxtwitter"

async def send_helper(message, twitter_links):
    name = get_name(message)
    content = f"**Sent by {name}**\n"
    for index, link in enumerate(twitter_links):
        if index > 0:
            content += f" {link}"
        else:
            content += f"{link}"

    helper_message = await message.channel.send(content=content)
    await edit_helper_message(helper_message, default_edit)
    await helper_message.edit(view=twitter_buttons(message, helper_message))

def get_name(message):
    member = message.author
    name = None
    if (member.global_name is not None):
        name = member.global_name
    else:
        name = member.name
    return name

def get_credit_embed(message):
    embed = discord.Embed(colour=discord.Color.from_rgb(r=0, g=168,b= 252))

    member = message.author
    name = None
    if (member.global_name is not None):
        name = member.global_name
    else:
        name = member.name

    embed.set_author(name=f"Sent by {name}", icon_url=str(member.display_avatar.url))
    return embed

def get_twitter_links(content):
    https_indices = get_link_indexes(content)
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

        return links
    else:
        return False

async def edit_helper_message(message, replacement):
    content = message.content
    https_indices = get_link_indexes(content)

    count = 0
    current_https = -1
    while count < len(https_indices):
        current_https = content.find("https", current_https + 1)
        starting_point = find_nth(content, "/", current_https, 2) + 1
        if content.find("www", current_https, current_https + 11) >= 0:
            ending_point = find_nth(content, ".", current_https, 2)
        else:
            ending_point = find_nth(content, ".", current_https, 1)
        content = content[:starting_point] + content[ending_point:]
        content = content[:starting_point] + replacement + content[starting_point:]
        count += 1

    await message.edit(content=content)

def get_link_indexes(content):
    https_indices = []
    search_index = 0
    while True:
        instance = content.find("https", search_index)
        if instance >= 0:
            search_index = instance + 1
            https_indices.append(instance)
        else:
            break
    return https_indices

def find_nth(content, to_find, start_index, occurence):
    current_amount = 0
    current_index = start_index
    final_index = None
    while current_amount < occurence:
        final_index = content.find(to_find, current_index)
        if final_index > -1:
            current_index = final_index + 1
        current_amount += 1
    return final_index

class twitter_buttons(View):
    def __init__(self, message, helper_message):
        self.message = message
        self.helper_message = helper_message
        View.__init__(self, timeout=button_time)

    async def on_timeout(self):
        try:
            await self.helper_message.edit(view=None)
        except:
            pass

    @discord.ui.button(label="vxtwitter", style=discord.ButtonStyle.secondary)
    async def vx_callback(self, interaction, button):
        if interaction.user == self.message.author:
            await edit_helper_message(interaction.message, "vxtwitter")
        await interaction.response.defer()

    @discord.ui.button(label="fxtwitter", style=discord.ButtonStyle.secondary)
    async def fx_callback(self, interaction, button):
        if interaction.user == self.message.author:
            await edit_helper_message(interaction.message, "fxtwitter")
        await interaction.response.defer()

    '''
    @discord.ui.button(label="fixupx", style=discord.ButtonStyle.secondary)
    async def fixupx_callback(self, interaction, button):
        if interaction.user == self.message.author:
            await edit_helper_message(interaction.message, "fixupx")
        await interaction.response.defer()
        '''

    @discord.ui.button(label="direct", style=discord.ButtonStyle.secondary)
    async def direct_callback(self, interaction, button):
        if interaction.user == self.message.author:
            await edit_helper_message(interaction.message, "twitter")
        await interaction.response.defer()

    @discord.ui.button(style=discord.ButtonStyle.red, emoji="✖️")
    async def delete_callback(self, interaction, button):
        if interaction.user == self.message.author:
            await self.helper_message.delete()
        await interaction.response.defer()