import discord
import discord.ui
from discord.ext import commands
from discord import app_commands

import config_access

class Debug(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        print("Initialized debug cog...")
    
    @commands.command()
    async def sync(self, ctx: commands.Context):
        # sync to the guild where the command was used
        ctx.bot.tree.copy_global_to(guild=ctx.guild)
        await ctx.bot.tree.sync(guild=ctx.guild)

        await ctx.send(content="Success")
        
    @commands.command()
    async def sync_global(self, ctx: commands.Context):
        # sync globally
        await ctx.bot.tree.sync()

        await ctx.send(content="Success")