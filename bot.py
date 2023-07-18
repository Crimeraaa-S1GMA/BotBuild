import discord
import discord.ui
from discord import app_commands
from discord.ext import commands
import asyncio
import threading
import config_access

import moderation
import memechannel
import susmode
import polls
import debug
import greetings

class BotBuildClient(commands.AutoShardedBot):
    async def on_ready(self):
        activity = discord.Activity(name="Made with BotBuild", type=discord.ActivityType.watching)
        await bot.change_presence(status=discord.Status.online, activity=activity)
        print("Welcome to BotBuild!")
        print("__________________________\n")
        print(f'Account: {self.user.name}!')
        
        print("__________________________\n")
        print("Initializing cogs...")
        
        if config_access.return_config_value("moderation_module_enabled"):
            await bot.add_cog(moderation.Moderation(self))
        
        if config_access.return_config_value("meme_channel_module_enabled"):
            await bot.add_cog(memechannel.MemeChannel(self))
        
        if config_access.return_config_value("sus_mode_easter_egg"):
            await bot.add_cog(susmode.SusMode(self))
        
        if config_access.return_config_value("polls_module_enabled"):
            await bot.add_cog(polls.Polls(self))
        
        if config_access.return_config_value("welcome_module_enabled"):
            await bot.add_cog(greetings.Greetings(self))
        
        await bot.add_cog(debug.Debug(self))

        print("__________________________\n")
        print("Ready!")



token_file = open("token.txt", "r")
loaded_token = token_file.read()

token_file.close()

intents = discord.Intents.all()

bot = BotBuildClient(intents=intents, command_prefix="!")

bot.run(loaded_token)
