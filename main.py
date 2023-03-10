import discord
import json
from discord import app_commands


class BotBuildClient(discord.Client):
    async def on_ready(self):
        activity = discord.Game(name="Made with BotBuild", type=3)
        await client.change_presence(status=discord.Status.online, activity=activity)
        await tree.sync(guild=discord.Object(id=1081978875178909787))
        print(f'Logged on as {self.user.name}!')

    async def on_guild_join(self, guild):
        channels = guild.text_channels
        await channels[0].send("@everyone WELLCUM")

    async def on_message(self, message):
        if message.author == client.user:
            return

        if ("suka" in message.content.lower() or "cyka" in message.content.lower()
                or "blya" in message.content.lower() or "сука" in message.content.lower()
                or "бля" in message.content.lower()) and config_json["cyka_blyat_easter_egg"]:
            await message.channel.send(config_json["cyka_blyat_answer"].format(member_mention=message.author.mention))

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

    # Reaction test
    async def on_raw_reaction_add(self, payload):
        message = await client.get_channel(payload.channel_id).fetch_message(payload.message_id)
        await message.clear_reactions()


config_file = open("bot_config.json", "r")
config_json = json.loads(config_file.read())

config_file.close()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.reactions = True

client = BotBuildClient(intents=intents)
tree = app_commands.CommandTree(client)


# Crappy test command
# @tree.command(name="balls", description="Test command", guild=discord.Object(id=1081978875178909787))
# async def first_command(interaction):
#    await interaction.response.send_message("Biggest balls of the summer\nIf you ain't cumming that's a bummer")


client.run(config_json["token"])
