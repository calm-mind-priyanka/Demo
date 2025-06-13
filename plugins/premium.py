# plugins/premium.py

from pyrogram import Client, filters
from pyrogram.types import Message
from database.users_chats_db import db
from datetime import datetime, timedelta
from info import ADMINS  # ✅ Importing admin list from info.py

# Add premium
@Client.on_message(filters.command("addpremium") & filters.user(ADMINS))
async def add_premium(client, message: Message):
    try:
        user_id = int(message.command[1])
        days = int(message.command[2])
    except (IndexError, ValueError):
        return await message.reply("❗ Correct usage: /addpremium user_id days")

    expiry = datetime.utcnow() + timedelta(days=days)
    await db.add_premium(user_id, expiry)
    await message.reply(f"✅ Added user `{user_id}` to Premium for {days} days.")

# Remove premium
@Client.on_message(filters.command("removepremium") & filters.user(ADMINS))
async def remove_premium(client, message: Message):
    try:
        user_id = int(message.command[1])
    except (IndexError, ValueError):
        return await message.reply("❗ Correct usage: /removepremium user_id")

    await db.remove_premium(user_id)
    await message.reply(f"❌ Removed Premium from user `{user_id}`.")

# My Plan
@Client.on_message(filters.command("myplan"))
async def my_plan(client, message: Message):
    user_id = message.from_user.id
    premium, expiry = await db.is_premium(user_id)

    if premium:
        await message.reply(f"✅ You are a Premium user.\n🗓️ Expiry: `{expiry.strftime('%Y-%m-%d')}`")
    else:
        await message.reply("⚠️ You are not a Premium user.\nType /start to view Premium plans.")
