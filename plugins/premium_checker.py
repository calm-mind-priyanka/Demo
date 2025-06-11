import json, time
from pyrogram import Client, filters
from pyrogram.types import Message

OWNER_ID = 6046055058  # your Telegram ID
PREMIUM_FILE = "premium_users.json"
BACKUP_CHANNEL = -1002763091823

def save_premium(data):
    with open(PREMIUM_FILE, "w") as f:
        json.dump(data, f, indent=2)

def load_premium():
    try:
        with open(PREMIUM_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def cleanup_expired_users():
    current = int(time.time())
    data = load_premium()
    before = len(data)
    updated = {uid: exp for uid, exp in data.items() if exp > current}
    if before != len(updated):
        save_premium(updated)
        return True, before - len(updated), updated
    return False, 0, updated

@Client.on_message(filters.command("checkpremium") & filters.private)
async def auto_expiry_check(client: Client, message: Message):
    if message.from_user.id != OWNER_ID:
        return await message.reply("🚫 You're not allowed to use this command.")

    cleaned, removed_count, updated = cleanup_expired_users()

    if cleaned:
        await client.send_document(
            chat_id=BACKUP_CHANNEL,
            document=PREMIUM_FILE,
            caption="🧹 Removed expired premium users."
        )
        await message.reply(f"✅ Cleaned {removed_count} expired premium users.")
    else:
        await message.reply("✅ No expired users found.")
