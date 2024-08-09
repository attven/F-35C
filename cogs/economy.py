import discord, sqlite3, json, datetime
from discord.ext import commands
from main import footer_text

from scripts.statistics import Statistics
stats = Statistics()

with open("./config.json", "r") as f:
    config = json.load(f)

# Add account
def account_add(user):
    with sqlite3.connect(config["db"]["economy"]) as conn:
        with conn:
            conn.execute("INSERT INTO accounts VALUES (?, ?)", (user, 100))
            conn.execute("INSERT INTO daily VALUES (?, ?)", (user, 0))

# Check if account exists
def is_account_exist(user):
    with sqlite3.connect(config["db"]["economy"]) as conn:
        with conn:
            cursor = conn.execute("SELECT * FROM accounts WHERE user = ?", (user,))
            if cursor.fetchone() is None:
                account_add(user)
                return False
            else:
                return True
            
# Get balance
def get_balance(user):
    is_account_exist(user)
    with sqlite3.connect(config["db"]["economy"]) as conn:
        with conn:
            cursor = conn.execute("SELECT balance FROM accounts WHERE user = ?", (user,))
            return cursor.fetchone()[0]

def get_daily(user):
    is_account_exist(user)
    with sqlite3.connect(config["db"]["economy"]) as conn:
        with conn:
            cursor = conn.execute("SELECT timestamp FROM daily WHERE user = ?", (user,))
            last_daily = cursor.fetchone()[0]

            if last_daily == 0 or datetime.datetime.now().timestamp() - last_daily > 86400:
                conn.execute("UPDATE daily SET timestamp = ? WHERE user = ?", (datetime.datetime.now().timestamp(), user))
                conn.execute("UPDATE accounts SET balance = ? WHERE user = ?", (get_balance(user) + 100, user))
                return "success"
            else:
                return "cooldown"

# Transfer money
def transfer(sender, receiver, amount):
    is_account_exist(sender)
    is_account_exist(receiver)
    sender_balance = get_balance(sender)

    if sender_balance < amount:
        return "insufficient"

    with sqlite3.connect(config["db"]["economy"]) as conn:
        with conn:
            conn.execute("UPDATE accounts SET balance = ? WHERE user = ?", (sender_balance - amount, sender))
            conn.execute("UPDATE accounts SET balance = ? WHERE user = ?", (get_balance(receiver) + amount, receiver))
            return "success"

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        with sqlite3.connect(config["db"]["economy"]) as conn:
            with conn:
                conn.execute("CREATE TABLE IF NOT EXISTS accounts (user INTEGER, balance INTEGER)")
                conn.execute("CREATE TABLE IF NOT EXISTS transactions (sender INTEGER, receiver INTEGER, amount INTEGER, timestamp INTEGER)")
                conn.execute("CREATE TABLE IF NOT EXISTS daily (user INTEGER, timestamp INTEGER)")
    
    # Check account balance
    @discord.slash_command(name= "balance", description= "Check your balance")
    async def balance(self, ctx: discord.ApplicationContext):
        is_account_exist(ctx.author.id)

        embed = discord.Embed(
            title= "Balance",
            description= f"Your balance is {get_balance(ctx.author.id)}",
            color= discord.Color.brand_green()
        )
        embed.set_footer(text= footer_text, icon_url= self.bot.user.avatar.url)

        await ctx.respond(embed= embed)
        stats.log_command("balance", ctx.author.id, ctx.channel.id, ctx.guild.id)
    
    # Transfer money
    @discord.slash_command(name= "transfer", description= "Transfer money to another user")
    async def transfer(self, ctx: discord.ApplicationContext, user: discord.User, amount: int):
        is_account_exist(ctx.author.id)
        is_account_exist(user.id)

        if transfer(ctx.author.id, user.id, amount) == "success":
            embed = discord.Embed(
                title= "Transfer funds",
                description= f"You have transferred {amount} to {user.mention}",
                color= discord.Color.brand_green()
            )
            embed.set_footer(text= footer_text, icon_url= self.bot.user.avatar.url)

            await ctx.respond(embed= embed)
            stats.log_command("transfer", ctx.author.id, ctx.channel.id, ctx.guild.id)
            stats.log_transaction(ctx.author.id, user.id, amount)
    
        else:
            embed = discord.Embed(
                title= "Transfer funds",
                description= f"You do not have enough money to transfer {amount} to {user.mention}",
                color= discord.Color.brand_green()
            )
            embed.set_footer(text= footer_text, icon_url= self.bot.user.avatar.url)

            await ctx.respond(embed= embed)
            stats.log_command("transfer", ctx.author.id, ctx.channel.id, ctx.guild.id)

    # Claim daily reward
    @discord.slash_command(name= "daily", description= "Claim your daily paycheck")
    async def daily(self, ctx: discord.ApplicationContext):
        if get_daily(ctx.author.id) == "success":
            embed = discord.Embed(
                title= "Daily paycheck",
                description= f"Claimed daily check",
                color= discord.Color.brand_green()
            )
            embed.add_field(name= "Balance", value= f"{get_balance(ctx.author.id)}", inline= True)
            embed.add_field(name= "Daily reward", value= "100", inline= True)
            embed.set_footer(text= footer_text, icon_url= self.bot.user.avatar.url)

            await ctx.respond(embed= embed)
            stats.log_command("daily", ctx.author.id, ctx.channel.id, ctx.guild.id)
            stats.log_event("claimed daily cash", ctx.author.id, ctx.channel.id, ctx.guild.id)
        
        else:
            embed = discord.Embed(
                title= "Daily paycheck",
                description= f"You have already claimed your daily check. Try again later.",
                color= discord.Color.brand_green()
            )
            embed.set_footer(text= footer_text, icon_url= self.bot.user.avatar.url)

            await ctx.respond(embed= embed)
            stats.log_command("daily", ctx.author.id, ctx.channel.id, ctx.guild.id)

def setup(bot):
    bot.add_cog(Economy(bot))
