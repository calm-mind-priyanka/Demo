import time
from pyrogram import Client
from info import BOT_TOKEN, API_ID, API_HASH

# Track uptime
StartTime = time.time()

# Bot version
__version__ = 1.1

# Initialize the main bot client
TechVJBot = Client(
    name="TechVJBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins={"root": "plugins"}
)
