import json
import os
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from info import ADMINS

FILENAME = "database/fsub.json"

def load_fsub():
    if os.path.exists(FILENAME):
        with open(FILENAME) as f:
            return json.load(f)
    return []

def save_fsub(channels):
    with open(FILENAME, "w") as f:
        json.dump(channels, f)

# ✅ Set Force Subscribe Channels
@Client.on_message(filters.command("setfsub") & filters.user(ADMINS))
async def set_fsub(client, message: Message):
    try:
        channel_ids = message.text.split(maxsplit=1)[1].split()
        save_fsub(channel_ids)
        await message.reply("✅ Force Subscribe channels updated successfully.")
    except Exception:
        await message.reply("❗ Usage:\n`/setfsub channel_id1 channel_id2 ...`")

# ❌ Delete Force Subscribe Settings
@Client.on_message(filters.command("delfsub") & filters.user(ADMINS))
async def del_fsub(client, message: Message):
    save_fsub([])
    await message.reply("❌ Force Subscribe requirement removed.")

# 🔍 Check FSub Logic
async def check_fsub(user_id, client):
    channels = load_fsub()
    not_joined = []

    for ch in channels:
        try:
            member = await client.get_chat_member(ch, user_id)
            if member.status not in ("member", "administrator", "creator"):
                not_joined.append(ch)
        except Exception as e:
            print(f"[FSub Error] {ch}: {e}")
            not_joined.append(ch)

    return not_joined

# 🔗 Send Join Buttons (Supports public and private)
async def send_join_buttons(client, message, not_joined):
    if not not_joined:
        return

    btns = []
    for c in not_joined:
        try:
            chat = await client.get_chat(c)
            if chat.username:
                # Public channel
                btns.append([InlineKeyboardButton("🔗 Join", url=f"https://t.me/{chat.username}")])
            else:
                # Private channel - generate invite link
                invite_link = await client.export_chat_invite_link(chat.id)
                btns.append([InlineKeyboardButton("🔗 Join", url=invite_link)])
        except Exception as e:
            print(f"[Join Button Error] {c}: {e}")

    btns.append([InlineKeyboardButton("✅ Joined", callback_data="refreshFsub")])

    await message.reply(
        "🚫 You must join the required channels to use this bot:",
        reply_markup=InlineKeyboardMarkup(btns)
    )

# 🔄 Refresh FSub Button
@Client.on_callback_query(filters.regex("refreshFsub"))
async def refresh_fsub(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    not_joined = await check_fsub(user_id, client)

    if not not_joined:
        await callback_query.message.edit("✅ Thank you! You're verified.")
    else:
        await callback_query.answer("🚫 Still missing some channels!", show_alert=True)
