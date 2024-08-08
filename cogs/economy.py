import discord, sqlite3
from discord.ext import commands
from main import footer_text

from scripts.stats import Statistics
stats = Statistics()

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_name = "database/economy.db"

        with sqlite3.connect(self.db_name) as conn:
            with conn:
                conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, balance INTEGER)")
    
    def is_account_exists(self, user_id):
        with sqlite3.connect(self.db_name) as conn:
            with conn:
                cursor = conn.execute("SELECT * FROM users WHERE id = ?", (user_id))
                if cursor.fetchone() is None:
                    self.create_account(user_id)
    
    def create_account(self, user_id):
        with sqlite3.connect(self.db_name) as conn:
            with conn:
                conn.execute("INSERT INTO users VALUES (?, ?)", (user_id, 0))

    @discord.slash_command(name= "balance", description= "Check your balance")
    async def balance(self, ctx: discord.ApplicationContext):
        self.is_account_exists(ctx.author.id)
        with sqlite3.connect(self.db_name) as conn:
            with conn:
                cursor = conn.execute("SELECT balance FROM users WHERE id = ?", (ctx.author.id))
                balance = cursor.fetchone()[0]
                await ctx.respond(embed= discord.Embed(
                    title= "Balance",
                    description= f"Your account balance: ${balance}",
                    color= discord.Color.brand_green()
                )
                .set_footer(text= footer_text, icon_url= self.bot.user.avatar.url)
                )
                stats.log_command("balance", ctx.author.id, ctx.channel.id, ctx.guild.id)
    
def setup(bot):
    bot.add_cog(Economy(bot))