import json
from pyrogram import Client, filters
from pyrogram.errors import UserNotParticipant
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

OWNER_ID = 6046055058
CHANNEL_FILE = "fsub_channels.json"

def load_channels():
    try:
        with open(CHANNEL_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_channels(data):
    with open(CHANNEL_FILE, "w") as f:
        json.dump(data, f)

@Client.on_message(filters.command("setfsub") & filters.private)
async def set_channels(bot: Client, message: Message):
    if message.from_user.id != OWNER_ID:
        return await message.reply("🚫 You can't use this command.")

    parts = message.text.strip().split()
    if len(parts) < 2:
        return await message.reply("❌ Usage: /setfsub <channel_id> <channel_id>")

    ids = parts[1:]
    save_channels(ids)
    await message.reply("✅ Force subscribe channels set successfully.")

@Client.on_message(filters.command("delfsub") & filters.private)
async def delete_fsub(bot: Client, message: Message):
    if message.from_user.id != OWNER_ID:
        return await message.reply("🚫 You can't use this command.")

    save_channels([])
    await message.reply("✅ All force subscribe channels removed.")

@Client.on_message(filters.private)
async def check_subscription(bot: Client, message: Message):
    if message.text and message.text.startswith("/"):
        return

    user_id = message.from_user.id
    not_joined = []
    channels = load_channels()

    for channel_id in channels:
        try:
            await bot.get_chat_member(int(channel_id), user_id)
        except UserNotParticipant:
            not_joined.append(channel_id)
        except:
            continue

    if not_joined:
        buttons = [[InlineKeyboardButton("Join Channel", url=f"https://t.me/c/{str(ch).replace('-100', '')}")] for ch in not_joined]
        await message.reply(
            "🚫 To use this bot, please join all required channels.",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
