from pyrogram import Client, filters
from TechVJ.util.premium_control import remove_premium
from info import ADMINS

@Client.on_message(filters.command("removepremium") & filters.user(ADMINS))
async def remove_premium_user(client, message):
    try:
        parts = message.text.split()
        if len(parts) != 2:
            return await message.reply("Format: /removepremium user_id")

        user_id = int(parts[1])
        remove_premium(user_id)
        await message.reply(f"❌ Removed user `{user_id}` from premium list.")
    except Exception as e:
        await message.reply(f"Error: {e}")
