import json
import discord
from discord.ext.commands import AutoShardedBot

def return_config_value(value):
    config_file = open("bot_config.json", "r")
    config_json = json.loads(config_file.read())

    config_file.close()

    return config_json[value]

def server_list(guilds):
    server_ids = []

    for guild in guilds:
        server_ids.append(discord.Object(guild.id))
    
    return server_ids