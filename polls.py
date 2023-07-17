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
    
    @app_commands.command()
    async def poll(self, interaction : discord.Interaction, channel : discord.TextChannel, question : str, answer_1 : str, answer_2 : str = "", answer_3 : str = "", answer_4 : str = "", answer_5 : str = ""):
        message = await channel.send(question)
        await interaction.response.send_message(f"Poll sent! {message.id}", ephemeral=True)