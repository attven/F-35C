import discord, sqlite3, json
from discord.ext import commands
from main import footer_text

from scripts.stats import Statistics
stats = Statistics()

# Apologies for the nested code

class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_name = "database/settings.db"

        # Create the database if it doesn't exist
        with sqlite3.connect(self.db_name) as conn:
            with conn:
                conn.execute("CREATE TABLE IF NOT EXISTS moderation (guild INTEGER, mod_channel INTEGER, logging BOOLEAN)")
    
        # All the commands in this bot are under the settings group
        settings = bot.create_group("settings")

        # Set the mod channel
        @settings.command(name= "mod_channel", description= "Set the mod channel")
        async def mod_channel(ctx: discord.ApplicationContext, channel: discord.TextChannel):
            with sqlite3.connect(self.db_name) as conn:
                with conn:
                    # Check if the guild is already in the database
                    cursor = conn.execute("SELECT * FROM moderation WHERE guild = ?", (ctx.guild.id,))
                    if cursor.fetchone() is None:
                        # Add the guild to the database
                        conn.execute("INSERT INTO moderation VALUES (?, ?, ?)", (ctx.guild.id, channel.id, False))
                    else:
                        # Update the guild in the database
                        conn.execute("UPDATE settings SET mod_channel = ? WHERE guild = ?", (channel.id, ctx.guild.id))

                    await ctx.respond(embed= discord.Embed(
                        title= "Mod channel set",
                        description= f"The mod channel has been set to {channel.mention}",
                        color= discord.Color.brand_green()
                    )
                    .set_footer(text= footer_text, icon_url= self.bot.user.avatar.url)
                    )

def setup(bot):
    bot.add_cog(Settings(bot))