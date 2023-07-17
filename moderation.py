import discord
import discord.ui
from discord.ext import commands
from discord import app_commands

import config_access

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

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        if config_access.return_config_value("moderation_module_enabled") and config_access.return_config_value("moderation_module_ban_enabled"):
            @bot.tree.command(name="ban", description="Bans a user")
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

        if config_access.return_config_value("moderation_module_enabled") and config_access.return_config_value("moderation_module_kick_enabled"):
            @bot.tree.command(name="kick", description="Kicks a user out of the server")
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

        if config_access.return_config_value("moderation_module_enabled") and config_access.return_config_value("moderation_module_dmsend_enabled"):
            @bot.tree.context_menu(name="Message")
            async def dmsend_ctxt(interaction : discord.Interaction, member : discord.Member):
                modal = SendMessage()
                modal.user_id = member.id
                await interaction.response.send_modal(modal)

        if config_access.return_config_value("moderation_module_enabled") and config_access.return_config_value("moderation_module_feature_enabled"):
            @bot.tree.context_menu(name="Feature Message")
            async def featuremsg_ctxt(interaction : discord.Interaction, message : discord.Message):
                channel = interaction.guild.get_channel(config_access.return_config_value("moderation_module_feature_channel"))

                embed = discord.Embed(title="Featured Message", description=message.content)
                embed.set_author(name=f"{message.author.name}", url=None, icon_url=message.author.avatar.url if message.author.avatar is not None else None)
                if len(message.attachments) > 0:
                    if message.attachments[0].content_type.startswith("image"):
                        embed.set_image(url=message.attachments[0].url)

                view = discord.ui.View()

                view.add_item(discord.ui.Button(label="Jump to message", url=message.jump_url))

                await channel.send(embed=embed, view=view)
                await interaction.response.send_message("Featured!", ephemeral=True)
        
        print("Initialized moderation cog...")
    
    @commands.hybrid_command()
    async def ping(self, ctx):
        await ctx.send("aaaaaa")