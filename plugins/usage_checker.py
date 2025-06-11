import json, time
from pyrogram import Client, filters
from pyrogram.types import Message

TRACKER_FILE = "usage_tracker.json"
PREMIUM_FILE = "premium_users.json"

def load_tracker():
    try:
        with open(TRACKER_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading tracker: {e}")
        return {}

def save_tracker(data):
    try:
        with open(TRACKER_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Error saving tracker: {e}")

def load_premium():
    try:
        with open(PREMIUM_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading premium list: {e}")
        return {}

@Client.on_message(filters.command("start"))
async def user_entry(client: Client, message: Message):
    user_id = str(message.from_user.id)
    premium = load_premium()

    if user_id in premium:
        return await message.reply("👑 You are a **premium user**.\nWelcome back!")

    tracker = load_tracker()
    today = time.strftime("%Y-%m-%d")

    if user_id in tracker and tracker[user_id] == today:
        return await message.reply("🕒 You've already used your **free access** today.\nTry again **tomorrow**.")
    
    tracker[user_id] = today
    save_tracker(tracker)
    await message.reply("✅ **Free access granted** for today!\nUpgrade to premium to use without limits.")
