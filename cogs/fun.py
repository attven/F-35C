import discord
from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # All the commands in this bot are under the fun group
        fun = bot.create_group("fun", "Fun commands")

        @fun.command(name= "httpcat", description= "HTTP status code cats")
        async def http_cat(ctx: discord.ApplicationContext, code: discord.Option(int, "Status code")): # type: ignore
            await ctx.respond(f"https://http.cat/{code}")

def setup(bot):
    bot.add_cog(Fun(bot))
