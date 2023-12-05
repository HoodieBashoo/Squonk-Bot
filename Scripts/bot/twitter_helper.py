import discord
from discord.ui import View

import webhooker
import guildprefs

default_edit = "fxtwitter"

async def send_helper(client, message, twitter_links):
    if message.channel.id == int(guildprefs.get_guild_pref(message.guild.id, "pinboard_channel")):
        return

    ''' For use in the case that you want the message to only post the links in the message
    content = ""
    for index, link in enumerate(twitter_links):
        if index > 0:
            content += f" {link}"
        else:
            content += f"{link}"
    '''
    content = message.content

    edited_content = edit_helper_content(content, default_edit)
    await webhooker.send_webhook_as_user(client, message.channel, edited_content, message.author, view=TwitterButtons(message.author, message.guild.id), wait=True)
    await message.delete()

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

def edit_helper_content(content, replacement):
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

    return content

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

# TODO: Buttons are now giving various errors if another person interacts with them
class TwitterButtons(View):
    def __init__(self, author, guild_id):
        self.author = author
        self.helper_message = None
        View.__init__(self, timeout=guildprefs.get_guild_pref(guild_id, "twitter_button_time"))

    async def on_timeout(self):
        try:
            await self.helper_message.edit(view=None)
        except AttributeError:
            print("Helper message does not exist, could not remove twitter helper buttons")

    def set_helper_message(self, message):
        self.helper_message = message

    @discord.ui.button(label="vxtwitter", style=discord.ButtonStyle.secondary)
    async def vx_callback(self, interaction, button):
        await self.helper_message.edit(content=edit_helper_content(interaction.message.content, "vxtwitter"))
        await interaction.response.defer()

    @discord.ui.button(label="fxtwitter", style=discord.ButtonStyle.secondary)
    async def fx_callback(self, interaction, button):
        await self.helper_message.edit(content=edit_helper_content(interaction.message.content, "fxtwitter"))
        await interaction.response.defer()

    '''
    @discord.ui.button(label="fixupx", style=discord.ButtonStyle.secondary)
    async def fixupx_callback(self, interaction, button):
        if interaction.user == self.message.author:
            await self.helper_message.edit(content=edit_helper_content(interaction.message.content, "fixupx"))
        else:
            await self.send_user_error(interaction)
        await interaction.response.defer()
        '''

    @discord.ui.button(label="direct", style=discord.ButtonStyle.secondary)
    async def direct_callback(self, interaction, button):
        await self.helper_message.edit(content=edit_helper_content(interaction.message.content, "twitter"))
        await interaction.response.defer()

    @discord.ui.button(style=discord.ButtonStyle.red, emoji="✖️")
    async def delete_callback(self, interaction, button):
        if interaction.user == self.author:
            await self.helper_message.delete()
        else:
            await self.send_user_error(interaction)
        await interaction.response.defer()

    async def send_user_error(self, interaction):
        await interaction.response.send_message("Sorry :( only the sender of the original tweet can do that", ephemeral=True)
