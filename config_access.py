import json
import discord

def return_config_value(value):
    config_file = open("bot_config.json", "r")
    config_json = json.loads(config_file.read())

    config_file.close()

    return config_json[value]

def server_list():
    config_file = open("bot_config.json", "r")
    config_json = json.loads(config_file.read())

    config_file.close()

    servers = config_json["servers"]
    server_ids = []

    for server in servers:
        server_ids.append(discord.Object(server))
    
    return server_ids