import json, time
from pyrogram import Client, filters
from pyrogram.types import Message

PREMIUM_FILE = "premium_users.json"

def load_premium():
    try:
        with open(PREMIUM_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

@Client.on_message(filters.command("myplan") & filters.private)
async def check_plan(bot: Client, message: Message):
    data = load_premium()
    user_id = str(message.from_user.id)

    if user_id in data and int(data[user_id]) > int(time.time()):
        remaining = int((int(data[user_id]) - time.time()) / 86400)
        await message.reply(f"👑 You are a premium user.\n⏳ Valid for: {remaining} more day(s).")
    else:
        await message.reply("⚠️ You are not a premium user.\n💳 Click /start and tap Show Plans to upgrade.")
