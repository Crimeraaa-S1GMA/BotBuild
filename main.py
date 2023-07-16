import discord
import discord.ui
from discord import app_commands
from discord.ext import commands
import asyncio
import threading
import config_access

import moderation

sussy_words = ["amogus", "sus", "vent", "sugoma", "imposter", "impasta", "lie", "liar", "electrical", "among"]

class BotBuildClient(commands.AutoShardedBot):
    async def on_ready(self):
        activity = discord.Activity(name="Made with BotBuild", type=discord.ActivityType.watching)
        await bot.change_presence(status=discord.Status.online, activity=activity)
        print("Welcome to BotBuild!")
        print("__________________________\n")
        print(f'Account: {self.user.name}!')
        
        print("__________________________\n")
        print("Initializing cogs...")
        
        await bot.add_cog(moderation.Moderation(self))
        for server in config_access.server_list(self.guilds):
            await self.tree.sync(guild=server)
        print("__________________________\n")
        print("Ready!")

    async def on_guild_join(self, guild):
        channels = guild.text_channels
        await channels[0].send("@everyone WELLCUM")

    async def on_message(self, message):
        if message.author == bot.user:
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
        await self.process_commands(message)

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
intents.message_content = True
intents.members = True
intents.guilds = True
intents.reactions = True

bot = BotBuildClient(intents=intents, command_prefix="!")

bot.run(loaded_token)
