import os, discord, json
from dotenv import load_dotenv
os.system('cls' if os.name == 'nt' else 'clear')

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

with open("./config.json", "r") as f:
    config = json.load(f)

if __name__ == "__main__":
    print(f"pwd: {os.getcwd()}")
    bot = discord.Bot()

    # Load commands
    for extension in config["extensions"]:
        bot.load_extension(f"scripts.cogs.{extension}")

    @bot.event
    async def on_ready():
        #Setting the bot presence
        await bot.change_presence(
            status= discord.Status.do_not_disturb,
            activity= discord.Activity(
                type= discord.ActivityType.playing,
                name= "with your life."
            )
        )

        print(f"Active as {bot.user}")
    
    bot.run(TOKEN)
