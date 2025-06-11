# Don't Remove Credit @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01

# Clone Code Credit : YT - @Tech_VJ / TG - @VJ_Bots / GitHub - @VJBots

import sys, glob, importlib.util, logging, logging.config, pytz, asyncio
from pathlib import Path
from datetime import date, datetime
from aiohttp import web

# ✅ Pyrogram Imports (fix was here)
from pyrogram import Client, filters, idle
from pyrogram.types import Message

# ✅ Local Imports
from TechVJ.bot import TechVJBot
from TechVJ.bot.clients import initialize_clients
from TechVJ.util.keepalive import ping_server
from plugins import web_server
from database.users_chats_db import db
from info import *
from utils import temp
from Script import script

# ✅ Backup channel to restore files
BACKUP_CHANNEL = -1002763091823  # Change this to your backup channel

# ✅ Logging setup
logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("imdbpy").setLevel(logging.ERROR)
logging.getLogger("aiohttp").setLevel(logging.ERROR)
logging.getLogger("aiohttp.web").setLevel(logging.ERROR)

# ✅ Restore premium & tracker JSON files from BACKUP_CHANNEL
@TechVJBot.on_message(filters.chat(BACKUP_CHANNEL) & filters.document)
async def restore_json_on_start(client, message: Message):
    if message.document.file_name in ["premium_users.json", "usage_tracker.json"]:
        await client.download_media(message)
        print(f"[RESTORE] {message.document.file_name} restored.")

# ✅ Start function
async def start():
    print("\nInitializing your bot...")

    await TechVJBot.start()
    bot_info = await TechVJBot.get_me()

    await initialize_clients()

    # Load all plugins dynamically from /plugins
    plugin_files = glob.glob("plugins/*.py")
    for plugin_path in plugin_files:
        plugin_name = Path(plugin_path).stem
        spec = importlib.util.spec_from_file_location(f"plugins.{plugin_name}", plugin_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        sys.modules[f"plugins.{plugin_name}"] = module
        print(f"✅ Imported plugin => {plugin_name}")

    # Set bot info in temp
    temp.BOT = TechVJBot
    temp.ME = bot_info.id
    temp.U_NAME = bot_info.username
    temp.B_NAME = bot_info.first_name

    # Send restart message
    tz = pytz.timezone('Asia/Kolkata')
    today = date.today()
    now = datetime.now(tz)
    time_str = now.strftime("%H:%M:%S %p")
    await TechVJBot.send_message(chat_id=LOG_CHANNEL, text=script.RESTART_TXT.format(today, time_str))

    # If running on Heroku, keep pinging
    if ON_HEROKU:
        asyncio.create_task(ping_server())

    # Start aiohttp web server
    app = web.AppRunner(await web_server())
    await app.setup()
    await web.TCPSite(app, "0.0.0.0", PORT).start()

    # Wait forever
    await idle()

# ✅ Main
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(start())
    except KeyboardInterrupt:
        logging.info("Service stopped. Bye 👋")
