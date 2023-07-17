import discord
import discord.ui
from discord.ext import commands
from discord import app_commands

import config_access

class MemeChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Initialized meme channel cog...")
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        
        if config_access.return_config_value("meme_channel_module_enabled") and message.channel.id == config_access.return_config_value("meme_channel"):
            if len(message.attachments) > 0:
                is_memes = True

                for att in message.attachments:
                    if not att.content_type.startswith("image") and not att.content_type.startswith("video"):
                        is_memes = False

                if is_memes:
                    await message.add_reaction("👍")
                    await message.add_reaction("👎")
                else:
                    await message.delete()
            else:
                await message.delete()