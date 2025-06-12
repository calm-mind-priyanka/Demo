import json, time
from pyrogram import Client, filters
from pyrogram.types import Message

PREMIUM_FILE = "premium_users.json"

def load_premium():
    try:
        with open(PREMIUM_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

@Client.on_message(filters.command("myplan") & filters.private)
async def check_premium(bot: Client, message: Message):
    user_id = str(message.from_user.id)
    data = load_premium()
    expiry = data.get(user_id)

    if expiry and int(expiry) > int(time.time()):
        remaining = int((int(expiry) - time.time()) / 86400)
        await message.reply(f"👑 You are a **premium user**.\n⏳ Days left: `{remaining}`")
    else:
        await message.reply("🚫 You are not a premium user.\n💳 Use /start and tap the **Show Plan** button to upgrade.")
