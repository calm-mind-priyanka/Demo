import json, time
from pyrogram import Client, filters
from pyrogram.types import Message

OWNER_ID = 6046055058  # your Telegram ID
BACKUP_CHANNEL = -1002763091823  # your private channel ID
PREMIUM_FILE = "premium_users.json"

def save_premium(data):
    with open(PREMIUM_FILE, "w") as f:
        json.dump(data, f, indent=2)  # prettier formatting

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

    parts = message.text.strip().split()
    if len(parts) != 3:
        return await message.reply("❌ Format:\n`/addpremium <user_id> <days>`")

    user_id = parts[1]
    if not user_id.isdigit():
        return await message.reply("❌ Invalid user_id format.")

    try:
        days = int(parts[2])
        expiry = int(time.time()) + days * 86400

        data = load_premium()
        existing = data.get(user_id)

        data[user_id] = expiry
        save_premium(data)

        await bot.send_document(
            chat_id=BACKUP_CHANNEL,
            document=PREMIUM_FILE,
            caption="📦 Premium users backup"
        )

        if existing:
            remaining = int((int(existing) - time.time()) / 86400)
            await message.reply(f"♻️ Updated premium for `{user_id}` by {days} day(s).\n🗓 Old Remaining: {remaining} days")
        else:
            await message.reply(f"✅ User `{user_id}` added as premium for {days} day(s).")

    except Exception as e:
        await message.reply(f"❌ Error: {e}")
