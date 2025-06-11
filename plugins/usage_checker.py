import json, time
from pyrogram import Client, filters
from pyrogram.types import Message

TRACKER_FILE = "usage_tracker.json"
PREMIUM_FILE = "premium_users.json"

def load_tracker():
    try:
        with open(TRACKER_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_tracker(data):
    with open(TRACKER_FILE, "w") as f:
        json.dump(data, f)

def load_premium():
    try:
        with open(PREMIUM_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

@Client.on_message(filters.command("start"))
async def user_entry(client: Client, message: Message):
    user_id = str(message.from_user.id)
    premium = load_premium()
    if user_id in premium:
        return await message.reply("👑 You are a premium user. Welcome!")

    tracker = load_tracker()
    today = str(time.strftime("%Y-%m-%d"))
    if user_id in tracker and tracker[user_id] == today:
        return await message.reply("🕒 You can only use this once per day.\nTry again tomorrow.")
    
    tracker[user_id] = today
    save_tracker(tracker)
    await message.reply("✅ Free access granted for today!")
