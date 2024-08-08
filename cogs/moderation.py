import discord, sqlite3
from discord.ext import commands
from main import footer_text

def get_mod_channel(self, guild_id):
    with sqlite3.connect("database/settings.db") as conn:
        with conn:
            cursor = conn.execute("SELECT mod_channel FROM moderation WHERE guild = ?", (guild_id))
            return cursor.fetchone()[0]

def check_logging_enabled(self, guild_id):
    with sqlite3.connect("database/settings.db") as conn:
        with conn:
            cursor = conn.execute("SELECT logging FROM moderation WHERE guild = ?", (guild_id))


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return

def setup(bot):
    bot.add_cog(Moderation(bot))