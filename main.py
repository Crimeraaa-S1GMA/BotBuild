from typing import Optional
import discord
import discord.ui
import json
from discord import app_commands
from discord.ext.commands import Bot
from discord.utils import MISSING
import config_access

sussy_words = ["amogus", "sus", "vent", "sugoma", "imposter", "impasta", "lie", "liar", "electrical", "among"]

class SendMessage(discord.ui.Modal, title='Send Message'):
    user_id = 0
    answer = discord.ui.TextInput(label='Message', style=discord.TextStyle.paragraph)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            user = interaction.client.get_user(self.user_id)
            embed = discord.Embed(title=f"Message from {interaction.guild.name}!", description=self.answer)
            embed.set_author(name=f"{interaction.user.name}", url=None, icon_url=interaction.user.avatar.url)
            await user.send(embed=embed)
            await interaction.response.send_message("Sent!", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message("Sending message failed!", ephemeral=True)

class BotBuildClient(discord.ext.commands.AutoShardedBot):
    async def on_ready(self):
        activity = discord.Activity(name="Made with BotBuild", type=discord.ActivityType.watching)
        await bot.change_presence(status=discord.Status.online, activity=activity)
        await bot.tree.sync(guild=discord.Object(id=1126581141642674267))
        print(f'Logged on as {self.user.name}!')

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

bot = BotBuildClient(intents=intents, command_prefix="/")

if config_access.return_config_value("moderation_module_enabled") and config_access.return_config_value("moderation_module_ban_enabled"):
    @bot.tree.command(name="ban", description="Bans a user", guilds=config_access.server_list())
    @app_commands.describe(reason="The reason you're banning the user for")
    async def ban_cmd(interaction : discord.Interaction, member : discord.Member, reason : str = ""):
        bot_member = await interaction.guild.fetch_member(bot.user.id)
        if interaction.permissions.ban_members:
            if member.top_role < bot_member.top_role and member.guild.owner.id != member.id:
                await member.ban(reason=reason)
                await interaction.response.send_message(f"Banned **{member.name}**", ephemeral=True)
            else:
                await interaction.response.send_message(f"Could not ban **{member.name}** due to role hierarchy", ephemeral=True)
        else:
            await interaction.response.send_message(f"Insufficient permissions to perform this action", ephemeral=True)

if config_access.return_config_value("moderation_module_enabled") and config_access.return_config_value("moderation_module_ban_from_context_menu_enabled"):
    @bot.tree.context_menu(name="Ban", guilds=config_access.server_list())
    async def ban_ctxt(interaction : discord.Interaction, member : discord.Member):
        bot_member = await interaction.guild.fetch_member(bot.user.id)
        if interaction.permissions.ban_members:
            if member.top_role < bot_member.top_role and member.guild.owner.id != member.id:
                await member.ban()
                await interaction.response.send_message(f"Banned **{member.name}**", ephemeral=True)
            else:
                await interaction.response.send_message(f"Could not ban **{member.name}** due to role hierarchy", ephemeral=True)
        else:
            await interaction.response.send_message(f"Insufficient permissions to perform this action", ephemeral=True)

if config_access.return_config_value("moderation_module_enabled") and config_access.return_config_value("moderation_module_kick_enabled"):
    @bot.tree.command(name="kick", description="Kicks a user out of the server", guilds=config_access.server_list())
    @app_commands.describe(reason="The reason you're kicking the user out for")
    async def kick_cmd(interaction : discord.Interaction, member : discord.Member, reason : str = ""):
        bot_member = await interaction.guild.fetch_member(bot.user.id)
        if interaction.permissions.kick_members:
            if member.top_role < bot_member.top_role and member.guild.owner.id != member.id:
                await member.kick(reason=reason)
                await interaction.response.send_message(f"Kicked **{member.name}** out", ephemeral=True)
            else:
                await interaction.response.send_message(f"Could not kick **{member.name}** out due to role hierarchy", ephemeral=True)
        else:
            await interaction.response.send_message(f"Insufficient permissions to perform this action", ephemeral=True)

if config_access.return_config_value("moderation_module_enabled") and config_access.return_config_value("moderation_module_kick_from_context_menu_enabled"):
    @bot.tree.context_menu(name="Kick", guilds=config_access.server_list())
    async def kick_ctxt(interaction : discord.Interaction, member : discord.Member):
        bot_member = await interaction.guild.fetch_member(bot.user.id)
        if interaction.permissions.kick_members:
            if member.top_role < bot_member.top_role and member.guild.owner.id != member.id:
                await member.kick()
                await interaction.response.send_message(f"Kicked **{member.name}** out", ephemeral=True)
            else:
                await interaction.response.send_message(f"Could not kick **{member.name}** out due to role hierarchy", ephemeral=True)
        else:
            await interaction.response.send_message(f"Insufficient permissions to perform this action", ephemeral=True)

if config_access.return_config_value("moderation_module_enabled") and config_access.return_config_value("moderation_module_dmsend_enabled"):
    @bot.tree.command(name="message", description="Sends a fancy message to a selected user", guilds=config_access.server_list())
    @app_commands.describe(member="The server member to send the message to", message="The content of the message you want to send")
    async def dmsend_cmd(interaction : discord.Interaction, member : discord.Member, message : str):
        try:
            embed = discord.Embed(title=f"Message from {interaction.guild.name}!", description=message)
            embed.set_author(name=f"{interaction.user.name}", url=None, icon_url=interaction.user.avatar.url)
            await member.send(embed=embed)
            await interaction.response.send_message("Sent!", ephemeral=True)
        except:
            await interaction.response.send_message("Sending message failed!", ephemeral=True)

if config_access.return_config_value("moderation_module_enabled") and config_access.return_config_value("moderation_module_dmsend_enabled"):
    @bot.tree.context_menu(name="Message", guilds=config_access.server_list())
    async def dmsend_ctxt(interaction : discord.Interaction, member : discord.Member):
        modal = SendMessage()
        modal.user_id = member.id
        await interaction.response.send_modal(modal)



bot.run(loaded_token)
