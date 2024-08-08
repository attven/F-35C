import discord
from discord.ext import commands
from main import footer_text

from scripts.statistics import Statistics
stats = Statistics()

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # Ping command
    @discord.slash_command(name= "ping", description= "Ping the bot")
    async def ping(self, ctx):
        await ctx.respond(embed= discord.Embed(
            title= "Pong!",
            description= f"Latency: {round(self.bot.latency * 1000)}ms",
            color= discord.Color.brand_green()
        )
        .set_footer(text= footer_text, icon_url= self.bot.user.avatar.url)
        )
        stats.log_command("ping", ctx.author.id, ctx.channel.id, ctx.guild.id)

def setup(bot):
    bot.add_cog(General(bot))