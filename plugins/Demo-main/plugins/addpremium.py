from pyrogram import Client, filters
from datetime import datetime, timedelta
import json

OWNER_ID = 6046055058  # ✅ replace with your Telegram user ID

@Client.on_message(filters.command("addpremium") & filters.user(OWNER_ID))
def add_premium_user(client, message):
    if len(message.command) != 3:
        message.reply_text("❗Correct format: /addpremium <user_id> <days>")
        return

    try:
        user_id = int(message.command[1])
        days = int(message.command[2])
    except ValueError:
        message.reply_text("❗Please use numbers: /addpremium <user_id> <days>")
        return

    expiry = (datetime.today() + timedelta(days=days)).strftime("%Y-%m-%d")

    try:
        with open("premium_users.json", "r") as f:
            data = json.load(f)
    except:
        data = {}

    data[str(user_id)] = expiry

    with open("premium_users.json", "w") as f:
        json.dump(data, f, indent=4)

    message.reply_text(
        f"✅ Added user `{user_id}` as premium for {days} days.\n"
        f"🗓️ Expires on: {expiry}"
    )
