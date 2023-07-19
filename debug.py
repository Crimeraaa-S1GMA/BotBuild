import discord
import discord.ui
from discord.ext import commands, tasks
from discord import app_commands

import config_access

class Debug(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dashboard_request_check.start()
        print("Initialized debug cog...")
    
    def cog_unload(self):
        self.dashboard_request_check.cancel()
    
    @tasks.loop(seconds=2.0)
    async def dashboard_request_check(self):
        req = ""

        with open("dashboard_req_to_bot", "r") as req_load:
            req = req_load.read().split()
        
        if "regcmd" in req:
            await self.bot.tree.sync()
            print("Registered slash commands!")
        
        with open("dashboard_req_to_bot", "w") as req_save:
            req_save.truncate()