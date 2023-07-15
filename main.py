import discord
import json
from discord import app_commands
from discord.ext.commands import Bot

sussy_words = ["amogus", "sus", "vent", "sugoma", "imposter", "impasta"]

class BotBuildClient(discord.ext.commands.Bot):
    async def on_ready(self):
        activity = discord.Activity(name="Made with BotBuild", type=discord.ActivityType.watching)
        await bot.change_presence(status=discord.Status.do_not_disturb, activity=activity)
        await bot.tree.sync(guild=discord.Object(id=1126581141642674267))
        print(f'Logged on as {self.user.name}!')

    async def on_guild_join(self, guild):
        channels = guild.text_channels
        await channels[0].send("@everyone WELLCUM")

    async def on_message(self, message):
        if message.author == bot.user:
            return
        
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
        if config_json["welcome_module_enabled"] and config_json["welcome_module_user_join_enabled"] \
                and member.guild == client.get_channel(config_json["welcome_module_join_channel"]).guild:
            channel = client.get_channel(config_json["welcome_module_join_channel"])
            await channel.send(config_json["welcome_module_user_join_message"].format(member_mention=member.mention))
            guild = member.guild
            for role_id in config_json["welcome_module_join_role_ids"]:
                role = guild.get_role(role_id)
                await member.add_roles(role)

    async def on_member_remove(self, member):
        if config_json["welcome_module_enabled"] and config_json["welcome_module_user_leave_enabled"] \
                and member.guild == client.get_channel(config_json["welcome_module_leave_channel"]).guild:
            channel = client.get_channel(config_json["welcome_module_leave_channel"])
            await channel.send(config_json["welcome_module_user_leave_message"].format(member_mention=member.mention))


config_file = open("bot_config.json", "r")
config_json = json.loads(config_file.read())

config_file.close()

token_file = open("token.txt", "r")
loaded_token = token_file.read()

token_file.close()

intents = discord.Intents.all()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.reactions = True

bot = BotBuildClient(intents=intents, command_prefix="/")

if config_json["moderation_module_enabled"] and config_json["moderation_module_ban_enabled"]:
    @bot.tree.command(name="ban", description="Bans a user", guild=discord.Object(1126581141642674267))
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

if config_json["moderation_module_enabled"] and config_json["moderation_module_ban_from_context_menu_enabled"]:
    @bot.tree.context_menu(name="Ban", guild=discord.Object(1126581141642674267))
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

if config_json["moderation_module_enabled"] and config_json["moderation_module_kick_enabled"]:
    @bot.tree.command(name="kick", description="Kicks a user out of the server", guild=discord.Object(1126581141642674267))
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

if config_json["moderation_module_enabled"] and config_json["moderation_module_kick_from_context_menu_enabled"]:
    @bot.tree.context_menu(name="Kick", guild=discord.Object(1126581141642674267))
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


bot.run(loaded_token)
