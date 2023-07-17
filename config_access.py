import json
import discord
from discord.ext.commands import AutoShardedBot

def return_config_value(value):
    config_file = open("bot_config.json", "r")
    config_json = json.loads(config_file.read())

    config_file.close()

    return config_json[value]