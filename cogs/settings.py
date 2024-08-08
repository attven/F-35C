import discord, sqlite3, json
from discord.ext import commands
from main import footer_text

from scripts.stats import Statistics
stats = Statistics()

# Apologies for the nested code, I'm afraid this is the only way to make it work.

class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_name = "database/settings.db"

        # Create the database if it doesn't exist
        with sqlite3.connect(self.db_name) as conn:
            with conn:
                conn.execute("CREATE TABLE IF NOT EXISTS settings (guild INTEGER, mod_channel INTEGER)")
    
        # All the commands in this bot are under the settings group
        settings = bot.create_group("settings")

        # Set the mod channel
        @settings.command(name= "mod_channel", description= "Set the mod channel")
        async def mod_channel(ctx: discord.ApplicationContext, channel: discord.TextChannel):
            with sqlite3.connect(self.db_name) as conn:
                with conn:
                    conn.execute("INSERT INTO settings VALUES (?, ?)", (ctx.guild.id, channel.id))
                    ctx.respond(embed= discord.Embed(
                        title= "Mod channel set",
                        description= f"The mod channel has been set to {channel.mention}",
                        color= discord.Color.brand_green()
                    )
                    .set_footer(text= footer_text, icon_url= self.bot.user.avatar.url)
                    )

def setup(bot):
    bot.add_cog(Settings(bot))