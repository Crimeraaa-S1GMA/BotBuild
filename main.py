import discord
import json
from discord import app_commands

sussy_words = ["amogus", "sus", "vent", "sugoma", "imposter", "impasta"]

class BotBuildClient(discord.Client):
    async def on_ready(self):
        activity = discord.Activity(name="Made with BotBuild", type=discord.ActivityType.watching)
        await client.change_presence(status=discord.Status.do_not_disturb, activity=activity)
        await tree.sync(guild=discord.Object(id=1126581141642674267))
        print(f'Logged on as {self.user.name}!')

    async def on_guild_join(self, guild):
        channels = guild.text_channels
        await channels[0].send("@everyone WELLCUM")

    async def on_message(self, message):
        if message.author == client.user:
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

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.reactions = True

client = BotBuildClient(intents=intents)
tree = app_commands.CommandTree(client)

    
@tree.command(name="test", description="This is a test command", guild=discord.Object(1126581141642674267))
async def test(interaction : discord.Interaction, member : discord.Member):
    await interaction.response.send_message("aaaaaaaaa")

# Crappy test command
# @tree.command(name="balls", description="Test command", guild=discord.Object(id=1081978875178909787))
# async def first_command(interaction):
#    await interaction.response.send_message("Biggest balls of the summer\nIf you ain't cumming that's a bummer")


client.run(loaded_token)
