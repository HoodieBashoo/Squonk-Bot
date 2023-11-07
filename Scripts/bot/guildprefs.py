import os.path
import json
from pathlib import Path

from botinfo import guild_data_path


default_prefs = {
    "prefix": "!",
    "userlog": False,
    "userlog_channel": 0,
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

        return True
    except:
        print(f"Critical Error! File does not exist at {full_path}")
        return False

def get_guild_pref(guild_id, preference):
    full_path = get_full_path(guild_id)
    try:
        with open(full_path, "r") as file:
            data = json.load(file)
            return data[preference]

        return True
    except:
        print(f"Critical Error! File does not exist at {full_path}")
        return False

def get_full_path(guild_id):
    filename = str(guild_id) + ".json"
    full_path = os.path.join(guild_data_path, filename)
    return full_path

#initialize_guild(1123123123123)
#edit_guild_pref(1123123123123, "prefix", "$")
#print(get_guild_pref(1123123123123, "prefix"))
