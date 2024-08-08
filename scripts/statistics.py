import datetime, sqlite3, json

with open("./config.json", "r") as f:
    config = json.load(f)

class Statistics:
    def __init__(self):
        with sqlite3.connect(config["db"]["statistics.db"]) as conn:
            with conn:
                conn.execute("CREATE TABLE IF NOT EXISTS commands (command TEXT, user INTEGER, channel INTEGER, guild INTEGER, timestamp TEXT)")
                conn.execute("CREATE TABLE IF NOT EXISTS events (event TEXT, timestamp TEXT)")
    
    def log_command(self, command, user, channel, guild):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S %d/%m/%Y")

        with sqlite3.connect(config["db"]["statistics.db"]) as conn:
            with conn:
                conn.execute("INSERT INTO commands VALUES (?, ?, ?, ?, ?)", (command, user, channel, guild, timestamp))
                print(f"{timestamp} | Logged command {command} by {user} in {channel}")
    
    def log_event(self, event):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S %d/%m/%Y")

        with sqlite3.connect(config["db"]["statistics.db"]) as conn:
            with conn:
                conn.execute("INSERT INTO events VALUES (?, ?)", (event, timestamp))
                print(f"{timestamp} | Logged event {event}")