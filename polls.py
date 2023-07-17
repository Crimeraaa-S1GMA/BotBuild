import discord
import discord.ui
from discord.ext import commands
from discord import app_commands

import config_access

class Polls(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Initialized poll cog...")
    
    @app_commands.command()
    async def poll(self, interaction : discord.Interaction, channel : discord.TextChannel, question : str, answer_1 : str, answer_2 : str, answer_3 : str = "", answer_4 : str = "", answer_5 : str = ""):
        view = discord.ui.View()
        select_menu = discord.ui.Select()
        select_menu.options.append(discord.SelectOption(label=answer_1, value="1"))
        select_menu.options.append(discord.SelectOption(label=answer_2, value="2"))
        if len(answer_3) > 0:
            select_menu.options.append(discord.SelectOption(label=answer_3, value="3"))
        if len(answer_4) > 0:
            select_menu.options.append(discord.SelectOption(label=answer_4, value="4"))
        if len(answer_5) > 0:
            select_menu.options.append(discord.SelectOption(label=answer_5, value="5"))
        view.add_item(select_menu)

        message = await channel.send(question, view=view)
        await interaction.response.send_message(f"Poll sent!", ephemeral=True)