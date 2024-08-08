import datetime, sqlite3

class Statistics:
    def __init__(self):
        self.db_name = "database/stats.db"
        
        with sqlite3.connect(self.db_name) as conn:
            with conn:
                conn.execute("CREATE TABLE IF NOT EXISTS commands (command TEXT, user INTEGER, channel INTEGER, guild INTEGER, timestamp TEXT)")
    
    def log_command(self, command, user, channel, guild):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S %d/%m/%Y")

        with sqlite3.connect(self.db_name) as conn:
            with conn:
                conn.execute("INSERT INTO commands VALUES (?, ?, ?, ?, ?)", (command, user, channel, guild, timestamp))