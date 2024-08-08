import discord, sqlite3, json
from discord.ext import commands
from main import footer_text

from scripts.statistics import Statistics
stats = Statistics()

with open("./config.json", "r") as f:
    config = json.load(f)

def is_settings_exist(guild):
    with sqlite3.connect(config["db"]["settings"]) as conn:
        with conn:
            cursor = conn.execute("SELECT * FROM moderation WHERE guild = ?", (guild,))
            
            if cursor.fetchone() is None:
                add_guild(guild)
                return False
            else:
                return True

def add_guild(guild):
    with sqlite3.connect(config["db"]["settings"]) as conn:
        with conn:
            conn.execute("INSERT INTO moderation VALUES (?, ?, ?)", (guild, 0, False))

class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_name = "database/settings.db"

        # Create the database if it doesn't exist
        with sqlite3.connect(self.db_name) as conn:
            with conn:
                conn.execute("CREATE TABLE IF NOT EXISTS moderation (guild INTEGER, mod_channel INTEGER, logging BOOLEAN)")
    
        # All the commands in this bot are under the settings group
        settings = bot.create_group("settings", "Bot settings")

        # Set the mod channel
        @settings.command(name= "mod_channel", description= "Set the mod channel")
        async def mod_channel(ctx: discord.ApplicationContext, channel: discord.TextChannel):
            with sqlite3.connect(self.db_name) as conn:
                with conn:
                    is_settings_exist(ctx.guild.id)
                    conn.execute("UPDATE moderation SET mod_channel = ? WHERE guild = ?", (channel.id, ctx.guild.id))

                    await ctx.respond(embed= discord.Embed(
                        title= "Mod channel set",
                        description= f"Mod channel set to {channel.mention}",
                        color= discord.Color.brand_green()
                    )
                    .set_footer(text= footer_text, icon_url= self.bot.user.avatar.url)
                    )
                    stats.log_command("mod_channel", ctx.author.id, ctx.channel.id, ctx.guild.id)
        
        # Toggle mod logging
        @settings.command(name= "mod_logging", description= "Toggle mod logging")
        async def mod_logging(
            ctx: discord.ApplicationContext,
            toggle: discord.Option(name= "toggle", description= "Toggle mod logging", choices= [
                    discord.OptionChoice(name= "enable", value= "True"),
                    discord.OptionChoice(name= "disable", value= "False")
                ]
            ) # type: ignore
        ):
            if toggle == "True":
                toggle = True
            else:
                toggle = False

            with sqlite3.connect(self.db_name) as conn:
                with conn:
                    is_settings_exist(ctx.guild.id)
                    conn.execute("UPDATE moderation SET logging = ? WHERE guild = ?", (toggle, ctx.guild.id))

                    await ctx.respond(embed= discord.Embed(
                        title= "Mod logging toggled",
                        description= f"Mod logging is now {toggle}",
                        color= discord.Color.brand_green()
                    )
                    .set_footer(text= footer_text, icon_url= ctx.author.avatar.url)
                    )
                    stats.log_command("mod_logging", ctx.author.id, ctx.channel.id, ctx.guild.id)

def setup(bot):
    bot.add_cog(Settings(bot))