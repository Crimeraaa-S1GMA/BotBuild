import discord
import discord.ui
from discord.ext import commands
from discord import app_commands

import config_access

class Polls(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        print("Initialized poll cog...")