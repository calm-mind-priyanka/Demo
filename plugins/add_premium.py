from pyrogram import Client, filters
from premium_control import add_premium  # ✅ Corrected
from info import ADMINS

@Client.on_message(filters.command("addpremium") & filters.user(ADMINS))
async def add_premium_user(client, message):
    try:
        parts = message.text.split()
        if len(parts) != 3:
            return await message.reply("Format: /addpremium user_id days")

        user_id = int(parts[1])
        days = int(parts[2])
        add_premium(user_id, days)
        await message.reply(f"✅ User `{user_id}` added to premium for `{days}` days.")
    except Exception as e:
        await message.reply(f"Error: {e}")
