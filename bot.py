import discord
import discord.ui
from discord import app_commands
from discord.ext import commands
import asyncio
import threading
import config_access
import json

import moderation
import memechannel
import susmode
import polls
import debug
import greetings

class BotBuildClient(commands.AutoShardedBot):
    async def on_ready(self):
        activity = discord.Activity(name="Made with BotBuild", type=discord.ActivityType.watching)
        await self.change_presence(status=discord.Status.online, activity=activity)
        print("Welcome to BotBuild!")
        print("__________________________\n")
        print(f'Account: {self.user.name}!')

        self.clean_servers()
        for server in self.guilds:
            self.add_server(server)
        
        print("__________________________\n")
        print("Initializing cogs...")
        
        if config_access.return_config_value("moderation_module_enabled"):
            await self.add_cog(moderation.Moderation(self))
        
        if config_access.return_config_value("meme_channel_module_enabled"):
            await self.add_cog(memechannel.MemeChannel(self))
        
        if config_access.return_config_value("sus_mode_easter_egg"):
            await self.add_cog(susmode.SusMode(self))
        
        if config_access.return_config_value("polls_module_enabled"):
            await self.add_cog(polls.Polls(self))
        
        if config_access.return_config_value("welcome_module_enabled"):
            await self.add_cog(greetings.Greetings(self))
        
        await self.add_cog(debug.Debug(self))

        print("__________________________\n")
        print("Ready!")
    
    def clean_servers(self):
        bot_cache = {}
        with open("bot_storage_cache.json", "r") as bot_cache_load:
            bot_cache = json.loads(bot_cache_load.read())
        
        bot_cache["servers"] = {}

        with open("bot_storage_cache.json", "w") as bot_cache_save:
            bot_cache_save.write(json.dumps(bot_cache, sort_keys=True, indent=4))
    
    def add_server(self, server : discord.Guild):
        bot_cache = {}
        with open("bot_storage_cache.json", "r") as bot_cache_load:
            bot_cache = json.loads(bot_cache_load.read())
        
        bot_cache["servers"][str(server.id)] = {
            "name" : server.name,
            "icon_url" : server.icon.url if server.icon is not None else ""
        }

        with open("bot_storage_cache.json", "w") as bot_cache_save:
            bot_cache_save.write(json.dumps(bot_cache, sort_keys=True, indent=4))
        


try:
    token_file = open("token.txt", "r")
    loaded_token = token_file.read()

    token_file.close()

    intents = discord.Intents.all()

    bot_client = BotBuildClient(intents=intents, command_prefix="!")
    bot_client.run(loaded_token)
except:
    print("Bot login failed. Check if you entered the correct token in the dashboard or the token.txt file.")


