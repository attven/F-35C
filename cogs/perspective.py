import discord, json
from discord.ext import commands
from main import footer_text

class Perspective(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(Perspective(bot))