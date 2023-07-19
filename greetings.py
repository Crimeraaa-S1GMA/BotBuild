import discord
import discord.ui
from discord.ext import commands
from discord import app_commands

import config_access

class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Initialized greetings cog...")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if config_access.return_config_value("welcome_module_enabled") and config_access.return_config_value("welcome_module_user_join_enabled"):
            channel = self.bot.get_channel(config_access.return_config_value("welcome_module_join_channel")[str(member.guild.id)])
            await channel.send(config_access.return_config_value("welcome_module_user_join_message").format(member_mention=member.mention))
            guild = member.guild
            for role_id in config_access.return_config_value("welcome_module_join_role_ids"):
                role = guild.get_role(role_id)
                await member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_member_remove(self, payload):
        if config_access.return_config_value("welcome_module_enabled") and config_access.return_config_value("welcome_module_user_leave_enabled"):
            channel = self.bot.get_channel(config_access.return_config_value("welcome_module_leave_channel")[str(payload.guild_id)])
            await channel.send(config_access.return_config_value("welcome_module_user_leave_message").format(member_mention=payload.user.mention))