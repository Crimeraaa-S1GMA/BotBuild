from typing import Optional
import discord
import discord.ui
from discord.ext import commands
from discord import app_commands

import config_access

class PollView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.select(custom_id="select_menu")
    async def select(self, interaction : discord.Interaction, select : discord.ui.Select):
        await interaction.response.send_message(f"Selected option {select.values[0]}!", ephemeral=True)

class Polls(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.add_view(PollView())
        print("Initialized poll cog...")
    
    @app_commands.command()
    async def poll(self, interaction : discord.Interaction, channel : discord.TextChannel, question : str, answer_1 : str, answer_2 : str, answer_3 : str = "", answer_4 : str = "", answer_5 : str = ""):
        view = PollView()
        view.children[0].options.append(discord.SelectOption(label=answer_1, value="1"))
        view.children[0].options.append(discord.SelectOption(label=answer_2, value="2"))
        if len(answer_3) > 0:
            view.children[0].options.append(discord.SelectOption(label=answer_3, value="3"))
        if len(answer_4) > 0:
            view.children[0].options.append(discord.SelectOption(label=answer_4, value="4"))
        if len(answer_5) > 0:
            view.children[0].options.append(discord.SelectOption(label=answer_5, value="5"))

        message = await channel.send(question, view=view)
        await interaction.response.send_message(f"Poll sent!", ephemeral=True)