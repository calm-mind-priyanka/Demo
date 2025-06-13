import os
import time
from pyrogram import Client, filters
from pyrogram.types import Message
from Script import script
from helper.utils import progress_for_pyrogram
from helper.database import daily_limit, add_user_to_db
from helper.premium_control import is_premium

DOWNLOAD_LOCATION = "./DOWNLOADS/"

@Client.on_message(filters.document & filters.private)
async def handle_file(client: Client, message: Message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    # Register user in database
    await add_user_to_db(user_id)

    # Check if user is premium
    premium = await is_premium(user_id)

    # Enforce daily limit for free users
    if not premium:
        allowed = await daily_limit(user_id)
        if not allowed:
            await message.reply_text(script.LIMIT)
            return

    # Create user download folder
    user_folder = os.path.join(DOWNLOAD_LOCATION, str(chat_id))
    os.makedirs(user_folder, exist_ok=True)

    # Get safe file name
    file_name = message.document.file_name or f"file_{message.document.file_id}"
    file_path = os.path.join(user_folder, file_name)

    # Download with progress bar
    start_time = time.time()
    try:
        await message.download(
            file_name=file_path,
            progress=progress_for_pyrogram,
            progress_args=(message, start_time, "Downloading...")
        )
    except Exception as e:
        await message.reply_text(f"❌ Error while downloading:\n`{e}`")
        return

    # Confirm download
    await message.reply_text(f"✅ File saved as `{file_name}`.\nNow generating your link...")
