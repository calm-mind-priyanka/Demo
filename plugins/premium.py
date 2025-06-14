from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
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

# My Plan (Advanced View)
@Client.on_message(filters.command("myplan"))
async def my_plan(client, message: Message):
    user_id = message.from_user.id
    premium, expiry = await db.is_premium(user_id)

    if premium and expiry:
        days_left = (expiry - datetime.utcnow()).days
        plan_text = (
            f"💎 **Premium Membership Details** 💎\n\n"
            f"👤 **User ID:** `{user_id}`\n"
            f"📅 **Expiry Date:** `{expiry.strftime('%Y-%m-%d')}`\n"
            f"⏳ **Days Remaining:** `{days_left}` day(s)\n\n"
            f"✅ Enjoy your premium features without limits!"
        )
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("✨ Upgrade Plan", url="https://t.me/YourSupportChannel")]
        ])
        await message.reply(plan_text, reply_markup=buttons)
    else:
        await message.reply("⚠️ You are not a Premium user.\nType /start to view Premium plans.")

# ✅ This function is needed for imports
async def is_premium(user_id: int) -> bool:
    premium, _ = await db.is_premium(user_id)
    return premium
