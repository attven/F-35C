import discord, sqlite3, json
from discord.ext import commands
from main import footer_text

from scripts.statistics import Statistics
stats = Statistics()

with open("./config.json", "r") as f:
    config = json.load(f)

def get_mod_channel(self, guild_id):
    with sqlite3.connect(config["db"]["settings"]) as conn:
        with conn:
            cursor = conn.execute("SELECT mod_channel FROM moderation WHERE guild = ?", (guild_id,))
            return cursor.fetchone()[0]

def is_logging_enabled(self, guild_id):
    with sqlite3.connect(config["db"]["settings"]) as conn:
        with conn:
            cursor = conn.execute("SELECT logging FROM moderation WHERE guild = ?", (guild_id,))
            if cursor.fetchone()[0] == 1:
                return True
            else:
                return False

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Log deleted messages
    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        if message.author.bot:
            return
        if is_logging_enabled(self, message.guild.id):
            mod_channel = get_mod_channel(self, message.guild.id)
            embed = discord.Embed(
                title= "Deleted by user",
                color= discord.Color.brand_red()
            )
            embed.set_author(name= message.author.name, icon_url= message.author.avatar.url)
            embed.add_field(name= "Message:", value= message.content, inline= False)

            embed.add_field(name= "In", value= message.channel.mention, inline= False)
            embed.set_footer(text= footer_text, icon_url= self.bot.user.avatar.url)

            await self.bot.get_channel(mod_channel).send(embed= embed)
            stats.log_event(f"sent by {message.author.id} in {message.channel.id}")
    
    # Log edited messages
    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if before.author.bot:
            return
        if is_logging_enabled(self, before.guild.id):
            mod_channel = get_mod_channel(self, before.guild.id)
            embed = discord.Embed(
                title= "Edited by user",
                color= discord.Color.brand_red()
            )
            embed.set_author(name= before.author.name, icon_url= before.author.avatar.url)
            embed.add_field(name= "Original:", value= before.content, inline= True)
            embed.add_field(name= "Now:", value= after.content, inline= True)

            embed.add_field(name= "Where", value= before.jump_url, inline= False)
            embed.set_footer(text= footer_text, icon_url= self.bot.user.avatar.url)
        
            await self.bot.get_channel(mod_channel).send(embed= embed)
            stats.log_event(f"sent by {before.author.id} in {before.channel.id}")

def setup(bot):
    bot.add_cog(Moderation(bot))
