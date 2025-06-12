import json, time
from pyrogram import Client, filters
from pyrogram.types import Message

OWNER_ID = 6046055058
PREMIUM_FILE = "premium_users.json"
BACKUP_CHANNEL = -1002763091823

def save_premium(data):
    with open(PREMIUM_FILE, "w") as f:
        json.dump(data, f)

def load_premium():
    try:
        with open(PREMIUM_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

@Client.on_message(filters.command("addpremium") & filters.private)
async def add_premium(bot: Client, message: Message):
    if message.from_user.id != OWNER_ID:
        return await message.reply("🚫 You are not allowed to use this command.")

    parts = message.text.strip().split()
    if len(parts) != 3 or not parts[1].isdigit() or not parts[2].isdigit():
        return await message.reply("❌ Invalid format.\n✅ Use: `/addpremium user_id days`")

    user_id = parts[1]
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
    await message.reply(f"✅ User `{user_id}` added as premium for {days} day(s).")
