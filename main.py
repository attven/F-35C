import os, discord, time, json
from dotenv import load_dotenv
from discord.ext import commands, bridge
os.system('cls' if os.name == 'nt' else 'clear')

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

with open("./config.json", "r") as f:
    config = json.load(f)

if __name__ == "__main__":
    print(f"pwd: {os.getcwd()}")
    time_log = {"start": None, "ready": None}
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

        # Logging
        print(f"Bot is online as {bot.user}")
        time_log["ready"] = round(time.time() - time_log["start"], 4)
        print(f"Active as {bot.user}, took {time_log['ready']}s")
    
    bot.run(TOKEN)
