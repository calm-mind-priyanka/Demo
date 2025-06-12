from pyrogram import Client, filters
from pyrogram.errors import UserNotParticipant
from pyrogram.types import Message

# List of channels users must join (editable using /setfsub or /delfsub)
FORCE_CHANNELS = ["@YourChannel1", "@YourChannel2"]

@Client.on_message(filters.private)
async def force_sub_check(bot: Client, message: Message):
    if message.text and message.text.startswith("/"):
        return  # Skip commands

    not_joined = []
    for channel in FORCE_CHANNELS:
        try:
            await bot.get_chat_member(channel, message.from_user.id)
        except UserNotParticipant:
            not_joined.append(channel)
        except Exception:
            continue

    if not_joined:
        text = "🚫 To use this bot, please join the required channels:\n"
        for ch in not_joined:
            text += f"👉 [Join Here]({ch})\n"
        await message.reply(text, disable_web_page_preview=True)
        return
