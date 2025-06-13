# plugins/fsub.py

import json
import os
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

# 🔐 Add your admin ID(s) here
ADMINS = [6046055058]

FILENAME = "database/fsub.json"

def load_fsub():
    if os.path.exists(FILENAME):
        with open(FILENAME) as f:
            return json.load(f)
    return []

def save_fsub(channels):
    with open(FILENAME, "w") as f:
        json.dump(channels, f)

# Set FSub
@Client.on_message(filters.command("setfsub") & filters.user(ADMINS))
async def set_fsub(client, message: Message):
    try:
        channel_ids = message.text.split(maxsplit=1)[1].split()
        save_fsub(channel_ids)
        await message.reply("✅ Force Subscribe channels updated.")
    except:
        await message.reply("❗ Usage: /setfsub channel_id1 channel_id2")

# Delete FSub
@Client.on_message(filters.command("delfsub") & filters.user(ADMINS))
async def del_fsub(client, message: Message):
    save_fsub([])
    await message.reply("❌ Force Subscribe requirement removed.")

# FSub check
async def check_fsub(user_id, client):
    channels = load_fsub()
    not_joined = []

    for ch in channels:
        try:
            member = await client.get_chat_member(ch, user_id)
            if member.status in ("left", "kicked"):
                not_joined.append(ch)
        except:
            not_joined.append(ch)

    return not_joined

async def send_join_buttons(client, message, not_joined):
    btns = [
        [InlineKeyboardButton("🔗 Join", url=f"https://t.me/{(await client.get_chat(c)).username}")]
        for c in not_joined
    ]
    btns.append([InlineKeyboardButton("✅ Joined", callback_data="refreshFsub")])
    await message.reply(
        "🚫 You must join the required channels to use this bot:",
        reply_markup=InlineKeyboardMarkup(btns)
    )
