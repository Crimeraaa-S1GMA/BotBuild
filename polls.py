from typing import Optional
import discord
import discord.ui
from discord.ext import commands
from discord import app_commands

import config_access

import json

def register_poll(message_id : int, question : str, answer_1 : str, answer_2 : str, answer_3 : str, answer_4 : str, answer_5 : str):
    with open("bot_data.json", "r") as file_r:
        bot_data = file_r.read()
    
    bot_data_json = json.loads(bot_data)

    bot_data_json["polls"][str(message_id)] = {
            "pollContent" : question,
            "pollAnswer1Content" : answer_1,
            "pollAnswer2Content" : answer_2,
            "pollAnswer3Content" : answer_3,
            "pollAnswer4Content" : answer_4,
            "pollAnswer5Content" : answer_5,
            "choice1Users" : [],
            "choice2Users" : [],
            "choice3Users" : [],
            "choice4Users" : [],
            "choice5Users" : [],
            "endTime" : 0
    }

    with open("bot_data.json", "w") as file_w:
        file_w.write(json.dumps(bot_data_json, sort_keys=True, indent=4))

def vote_on_poll(message_id : int, user_id : int, choice : str):
    with open("bot_data.json", "r") as file_r:
        bot_data = file_r.read()
    
    bot_data_json = json.loads(bot_data)

    if user_id in bot_data_json["polls"][str(message_id)]["choice1Users"]:
        bot_data_json["polls"][str(message_id)]["choice1Users"].remove(user_id)
    if user_id in bot_data_json["polls"][str(message_id)]["choice2Users"]:
        bot_data_json["polls"][str(message_id)]["choice2Users"].remove(user_id)
    if user_id in bot_data_json["polls"][str(message_id)]["choice3Users"]:
        bot_data_json["polls"][str(message_id)]["choice3Users"].remove(user_id)
    if user_id in bot_data_json["polls"][str(message_id)]["choice4Users"]:
        bot_data_json["polls"][str(message_id)]["choice4Users"].remove(user_id)
    if user_id in bot_data_json["polls"][str(message_id)]["choice5Users"]:
        bot_data_json["polls"][str(message_id)]["choice5Users"].remove(user_id)
    
    bot_data_json["polls"][str(message_id)][choice].append(user_id)

    with open("bot_data.json", "w") as file_w:
        file_w.write(json.dumps(bot_data_json, sort_keys=True, indent=4))

def get_poll_options(message_id : int):
    with open("bot_data.json", "r") as file_r:
        bot_data = file_r.read()
    
    bot_data_json = json.loads(bot_data)

    len_1 = len(bot_data_json["polls"][str(message_id)]["choice1Users"])
    len_2 = len(bot_data_json["polls"][str(message_id)]["choice2Users"])
    len_3 = len(bot_data_json["polls"][str(message_id)]["choice3Users"])
    len_4 = len(bot_data_json["polls"][str(message_id)]["choice4Users"])
    len_5 = len(bot_data_json["polls"][str(message_id)]["choice5Users"])

    content = bot_data_json["polls"][str(message_id)]["pollContent"]
    answer_1 = bot_data_json["polls"][str(message_id)]["pollAnswer1Content"]
    answer_2 = bot_data_json["polls"][str(message_id)]["pollAnswer2Content"]
    answer_3 = bot_data_json["polls"][str(message_id)]["pollAnswer3Content"]
    answer_4 = bot_data_json["polls"][str(message_id)]["pollAnswer4Content"]
    answer_5 = bot_data_json["polls"][str(message_id)]["pollAnswer5Content"]

    return [len_1, len_2, len_3, len_4, len_5, len_1 + len_2 + len_3 + len_4 + len_5, content, answer_1, answer_2, answer_3, answer_4, answer_5]

class PollView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.select(custom_id="select_menu")
    async def select(self, interaction : discord.Interaction, select : discord.ui.Select):
        choice_to_json_choice = "choice1Users"
        if select.values[0] == "1":
            choice_to_json_choice = "choice1Users"
        if select.values[0] == "2":
            choice_to_json_choice = "choice2Users"
        if select.values[0] == "3":
            choice_to_json_choice = "choice3Users"
        if select.values[0] == "4":
            choice_to_json_choice = "choice4Users"
        if select.values[0] == "5":
            choice_to_json_choice = "choice5Users"
        vote_on_poll(interaction.message.id, interaction.user.id, choice_to_json_choice)
        poll_options = get_poll_options(interaction.message.id)
        message_content = f"# **Poll: {poll_options[6]}**\n"
        message_content += f"\n{poll_options[7]} - `{(poll_options[0] / poll_options[5]) * 100.0}%`"
        message_content += f"\n{poll_options[8]} - `{(poll_options[1] / poll_options[5]) * 100.0}%`"
        if len(poll_options[9]) > 0:
            message_content += f"\n{poll_options[9]} - `{(poll_options[2] / poll_options[5]) * 100.0}%`"
        if len(poll_options[10]) > 0:
            message_content += f"\n{poll_options[10]} - `{(poll_options[3] / poll_options[5]) * 100.0}%`"
        if len(poll_options[11]) > 0:
            message_content += f"\n{poll_options[11]} - `{(poll_options[4] / poll_options[5]) * 100.0}%`"
        await interaction.message.edit(content=message_content)
        await interaction.response.send_message(f"Selected option {select.values[0]}!", ephemeral=True)

class Polls(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.add_view(PollView())
        print("Initialized poll cog...")
    
    @app_commands.command()
    async def poll(self, interaction : discord.Interaction, channel : discord.TextChannel, question : str, answer_1 : str, answer_2 : str, answer_3 : str = "", answer_4 : str = "", answer_5 : str = ""):
        view = PollView()
        view.children[0].options.append(discord.SelectOption(label=answer_1, value="1"))
        view.children[0].options.append(discord.SelectOption(label=answer_2, value="2"))
        if len(answer_3) > 0:
            view.children[0].options.append(discord.SelectOption(label=answer_3, value="3"))
        if len(answer_4) > 0:
            view.children[0].options.append(discord.SelectOption(label=answer_4, value="4"))
        if len(answer_5) > 0:
            view.children[0].options.append(discord.SelectOption(label=answer_5, value="5"))

        message_content = f"# **Poll: {question}**\n"
        message_content += f"\n{answer_1} - `0%`"
        message_content += f"\n{answer_2} - `0%`"
        if len(answer_3) > 0:
            message_content += f"\n{answer_3} - `0%`"
        if len(answer_4) > 0:
            message_content += f"\n{answer_4} - `0%`"
        if len(answer_5) > 0:
            message_content += f"\n{answer_5} - `0%`"

        message = await channel.send(message_content, view=view)
        register_poll(message.id, question, answer_1, answer_2, answer_3, answer_4, answer_5)
        await interaction.response.send_message(f"Poll sent!", ephemeral=True)