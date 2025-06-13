from pyrogram import Client, filters
from pyrogram.types import Message
import json
from datetime import datetime, timezone

@Client.on_message(filters.command("myplan") & filters.private)
async def check_plan(client: Client, message: Message):
    try:
        with open("premium.json", "r") as f:
            premium_data = json.load(f)
    except:
        premium_data = {}

    user_id = str(message.from_user.id)
    expiry_str = premium_data.get(user_id)

    if expiry_str:
        try:
            expiry_time = datetime.fromisoformat(expiry_str).replace(tzinfo=timezone.utc)
            now = datetime.now(timezone.utc)

            if now < expiry_time:
                days_left = (expiry_time - now).days
                await message.reply(
                    f"👑 You are a premium user.\n⏳ Valid for: {days_left} more day(s).\n📅 Expires on: {expiry_time.date()}"
                )
                return
        except Exception as e:
            await message.reply(f"⚠️ Error parsing date for your premium: {e}")

    await message.reply("⚠️ You are not a premium user.\n💳 Click /start and tap Show Plans to upgrade.")
