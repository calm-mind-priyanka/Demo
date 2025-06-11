import json, time
from pyrogram import Client, filters
from pyrogram.types import Message

OWNER_ID = 6046055058  # your Telegram ID
BACKUP_CHANNEL = -1002763091823  # your private channel ID
PREMIUM_FILE = "premium_users.json"

def save_premium(data):
    with open(PREMIUM_FILE, "w") as f:
        json.dump(data, f)

def load_premium():
    try:
        with open(PREMIUM_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

@Client.on_message(filters.command("addpremium") & filters.private)
async def add_premium_user(bot: Client, message: Message):
    if message.from_user.id != OWNER_ID:
        return await message.reply("🚫 You're not allowed to use this command.")

    parts = message.text.split()
    if len(parts) != 3:
        return await message.reply("❌ Format:\n`/addpremium <user_id> <days>`")

    user_id = str(parts[1])
    try:
        days = int(parts[2])
        expiry = int(time.time()) + days * 86400
        data = load_premium()
        data[user_id] = expiry
        save_premium(data)

        await bot.send_document(
            chat_id=BACKUP_CHANNEL,
            document=PREMIUM_FILE,
            caption="📦 Premium users backup"
        )
        await message.reply(f"✅ User `{user_id}` added for {days} day(s).")
    except:
        await message.reply("❌ Invalid user_id or days.")
