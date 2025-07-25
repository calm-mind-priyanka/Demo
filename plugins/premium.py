from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from database.users_chats_db import db
from datetime import datetime, timedelta
from info import ADMINS  # ✅ Importing admin list from info.py

# ✅ Add Premium
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

# ❌ Remove Premium
@Client.on_message(filters.command("removepremium") & filters.user(ADMINS))
async def remove_premium(client, message: Message):
    try:
        user_id = int(message.command[1])
    except (IndexError, ValueError):
        return await message.reply("❗ Correct usage: /removepremium user_id")

    await db.remove_premium(user_id)
    await message.reply(f"❌ Removed Premium from user `{user_id}`.")

# 📦 My Plan Status
@Client.on_message(filters.command("myplan"))
async def my_plan(client, message: Message):
    user_id = message.from_user.id
    premium, expiry = await db.is_premium(user_id)

    if premium:
        days_remaining = (expiry - datetime.utcnow()).days
        await message.reply(
            f"✨ **Your Premium Plan Details:**\n\n"
            f"✅ **Status:** Active Premium\n"
            f"📅 **Expires on:** `{expiry.strftime('%Y-%m-%d')}`\n"
            f"⏳ **Days Left:** `{days_remaining}` day(s)\n\n"
            f"🔓 Features:\n"
            f"- Unlimited File Links\n"
            f"- No Ads\n"
            f"- Fastest Speeds",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💎 Upgrade Plan", url="https://t.me/Sandymaiwait")]
            ])
        )
    else:
        await message.reply(
            "⚠️ You are not a Premium user.\n\n"
            "💡 Unlock exclusive features like:\n"
            "- 🚫 No Ads\n"
            "- 🔗 Unlimited File Links\n"
            "- ⚡ Fastest Speeds\n\n"
            "Click below to get Premium now ⬇️",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💎 Upgrade Plan", url="https://t.me/Sandymaiwait")]
            ])
        )

# ✅ This function is used in other files to check status
async def is_premium(user_id: int) -> bool:
    premium, _ = await db.is_premium(user_id)
    return premium
