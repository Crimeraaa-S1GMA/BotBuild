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
        
        for server in config_access.server_list(self.guilds):
            await self.tree.sync(guild=server)
        print("__________________________\n")
        print("Ready!")

    async def on_member_join(self, member):
        if config_access.return_config_value("welcome_module_enabled") and config_access.return_config_value("welcome_module_user_join_enabled") \
                and member.guild == bot.get_channel(config_access.return_config_value("welcome_module_join_channel")).guild:
            channel = bot.get_channel(config_access.return_config_value("welcome_module_join_channel"))
            await channel.send(config_access.return_config_value("welcome_module_join_message").format(member_mention=member.mention))
            guild = member.guild
            for role_id in config_access.return_config_value("welcome_module_join_role_ids"):
                role = guild.get_role(role_id)
                await member.add_roles(role)

    async def on_member_remove(self, member):
        if config_access.return_config_value("welcome_module_enabled") and config_access.return_config_value("welcome_module_user_leave_enabled") \
                and member.guild == bot.get_channel(config_access.return_config_value("welcome_module_leave_channel")).guild:
            channel = bot.get_channel(config_access.return_config_value("welcome_module_leave_channel"))
            await channel.send(config_access.return_config_value("welcome_module_leave_message").format(member_mention=member.mention))



token_file = open("token.txt", "r")
loaded_token = token_file.read()

token_file.close()

intents = discord.Intents.all()

bot = BotBuildClient(intents=intents, command_prefix="!")

bot.run(loaded_token)
