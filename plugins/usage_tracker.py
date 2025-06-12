import json, time
from pyrogram import Client, filters
from pyrogram.types import Message

USAGE_FILE = "usage_tracker.json"
PREMIUM_FILE = "premium_users.json"

def load_json(file):
    try:
        with open(file, "r") as f:
            return json.load(f)
    except:
        return {}

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f)

@Client.on_message(filters.private & filters.document)
async def limit_free_users(bot: Client, message: Message):
    user_id = str(message.from_user.id)
    usage = load_json(USAGE_FILE)
    premium = load_json(PREMIUM_FILE)

    now = int(time.time())
    is_premium = user_id in premium and premium[user_id] > now

    if is_premium:
        return  # Let premium users continue normally

    last_used = usage.get(user_id)
    today = time.strftime("%Y-%m-%d", time.localtime(now))

    if last_used == today:
        await message.reply(
            "❌ Free users can generate only 1 link per day.\n\n💳 Click /start and tap the **Show Plans** button to upgrade."
        )
        return

    # First time today
    usage[user_id] = today
    save_json(USAGE_FILE, usage)
    # Proceed with file handling logic (bot continues)
