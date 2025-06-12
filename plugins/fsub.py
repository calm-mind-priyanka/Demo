from pyrogram import Client, filters
from pyrogram.types import Message
from info import ADMINS, FSUB_CHANNELS

@Client.on_message(filters.command("setfsub") & filters.user(ADMINS))
async def set_fsub(client, message: Message):
    try:
        ids = message.text.split()[1:]
        if not ids:
            return await message.reply("Use: /setfsub -100123456789 -100987654321")
        with open("fsub.json", "w") as f:
            import json
            json.dump({"channels": ids}, f)
        await message.reply("✅ Force subscribe channels set.")
    except Exception as e:
        await message.reply(f"Error: {e}")

@Client.on_message(filters.command("delsub") & filters.user(ADMINS))
async def del_fsub(client, message: Message):
    import os
    if os.path.exists("fsub.json"):
        os.remove("fsub.json")
        await message.reply("❌ Force subscribe removed.")
    else:
        await message.reply("No force subscribe set.")
