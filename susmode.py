import discord
import discord.ui
from discord.ext import commands
from discord import app_commands

import config_access

sussy_words = ["amogus", "sus", "vent", "sugoma", "imposter", "impasta", "lie", "liar", "electrical", "among"]

class SusMode(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        print("Initialized sus mode cog...")
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if config_access.return_config_value("sus_mode_easter_egg") and (len(config_access.return_config_value("sus_mode_channels")) < 1 or message.channel.id in config_access.return_config_value("sus_mode_channels")):
            found_sus = False

            for word in sussy_words:
                if word in message.content.lower().replace(" ", "").replace("\n", ""):
                    found_sus = True
            
            if found_sus:
                await message.add_reaction("🤨")
                await message.add_reaction("🇸")
                await message.add_reaction("🇺")
                await message.add_reaction("5️⃣")
                await message.channel.send("SUS! :face_with_raised_eyebrow:")

