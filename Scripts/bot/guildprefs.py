import os
import os.path
import json

from botinfo import guild_data_path


default_prefs = {
    "prefix": "s!",
    "userlog": False,
    "userlog_channel": 0,
    "pinboard": False,
    "pinboard_channel": 0,
    "pin_activation_emoji": "",
    "twithelper": False,
    "twitter_button_time": 0
}

def initialize_guild(guild_id):
    full_path = get_full_path(guild_id)
    if os.path.isfile(full_path):
        print(f"{guild_id}.json has already been created!")
    else:
        with open(full_path, "w") as file:
            json.dump(default_prefs, file, indent=4)

def edit_guild_pref(guild_id, preference, new_data):
    full_path = get_full_path(guild_id)
    try:
        with open(full_path, "r+") as file:
            data = json.load(file)
            data[preference] = new_data

            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()
    except FileNotFoundError:
        print(f"Critical Error! File does not exist at {full_path}")

def get_guild_pref(guild_id, preference):
    full_path = get_full_path(guild_id)
    try:
        with open(full_path, "r") as file:
            data = json.load(file)
            return data[preference]
    except FileNotFoundError:
        print(f"Critical Error! File does not exist at {full_path}")
        return False

def get_guild_prefs(guild_id):
    full_path = get_full_path(guild_id)
    try:
        with open(full_path, "r") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"Critical Error! File does not exist at {full_path}")
        return False

def update_guild_pref_data(client):
    for guild in client.guilds:
        print(f"updating guild pref data on guild {guild.name}")
        full_path = get_full_path(guild.id)
        try:
            with open(full_path, "r+") as file:
                data = json.load(file)

                for default_pref in default_prefs:
                    found_pref = False
                    for pref in data:
                        if pref == default_pref:
                            found_pref = True
                            break
                    if found_pref is False:
                        data[default_pref] = default_prefs[default_pref]

                file.seek(0)
                json.dump(data, file, indent=4)
                file.truncate()
                print("Successfully updated")
        except FileNotFoundError:
            print(f"Could not find file for {guild.name} while updating guild pref data. Creating...")
            initialize_guild(guild.id)

def get_full_path(guild_id):
    filename = str(guild_id) + ".json"
    full_path = os.path.join(guild_data_path, filename)
    return full_path
