import json, time
from pyrogram import Client, filters
from pyrogram.types import Message

PREMIUM_FILE = "premium_users.json"
BACKUP_CHANNEL = -1002763091823

def save_premium(data):
    with open(PREMIUM_FILE, "w") as f:
        json.dump(data, f)

def load_premium():
    try:
        with open(PREMIUM_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def cleanup_expired_users():
    current = int(time.time())
    data = load_premium()
    updated = {uid: exp for uid, exp in data.items() if exp > current}
    if len(data) != len(updated):
        save_premium(updated)
    return updated

@Client.on_message(filters.text)
async def auto_expiry_check(client: Client, message: Message):
    updated = cleanup_expired_users()
    await client.send_document(
        chat_id=BACKUP_CHANNEL,
        document=PREMIUM_FILE,
        caption="📦 Cleaned premium list (expired removed)"
    )
