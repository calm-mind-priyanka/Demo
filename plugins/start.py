import random
import humanize
from Script import script
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from info import URL, LOG_CHANNEL, SHORTLINK
from urllib.parse import quote_plus
from TechVJ.util.file_properties import get_name, get_hash, get_media_file_size
from TechVJ.util.human_readable import humanbytes
from TechVJ.util.premium_control import can_generate_link
from database.users_chats_db import db
from utils import temp, get_shortlink

# /start command handler
@Client.on_message(filters.command("start") & filters.incoming)
async def start(client, message):
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
        await client.send_message(
            LOG_CHANNEL,
            script.LOG_TEXT_P.format(message.from_user.id, message.from_user.mention)
        )

    rm = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎯 Show Plans", callback_data="plans")],
        [
            InlineKeyboardButton("♻️ Renew Premium", callback_data="renew"),
            InlineKeyboardButton("💳 Get Premium", callback_data="buy")
        ],
        [InlineKeyboardButton("📞 Contact Support", url="https://t.me/KingVJ01")]
    ])

    await client.send_message(
        chat_id=message.from_user.id,
        text=script.START_TXT.format(message.from_user.mention, temp.U_NAME, temp.B_NAME),
        reply_markup=rm,
        parse_mode=enums.ParseMode.HTML
    )


# Media upload handler
@Client.on_message(filters.private & (filters.document | filters.video))
async def stream_start(client, message):
    user_id = message.from_user.id
    username = message.from_user.mention

    # ✅ Premium check
    if not await can_generate_link(user_id):
        await message.reply_text(
            "⚠️ You’ve already used your free link today.\n\n💳 To get unlimited access, consider buying premium from /plan.",
            quote=True
        )
        return

    file = getattr(message, message.media.value)
    filename = file.file_name
    filesize = humanize.naturalsize(file.file_size)
    fileid = file.file_id

    log_msg = await client.send_cached_media(
        chat_id=LOG_CHANNEL,
        file_id=fileid,
    )

    fileName = quote_plus(get_name(log_msg))

    if not SHORTLINK:
        stream = f"{URL}watch/{log_msg.id}/{fileName}?hash={get_hash(log_msg)}"
        download = f"{URL}{log_msg.id}/{fileName}?hash={get_hash(log_msg)}"
    else:
        stream = await get_shortlink(f"{URL}watch/{log_msg.id}/{fileName}?hash={get_hash(log_msg)}")
        download = await get_shortlink(f"{URL}{log_msg.id}/{fileName}?hash={get_hash(log_msg)}")

    await log_msg.reply_text(
        text=f"•• ʟɪɴᴋ ɢᴇɴᴇʀᴀᴛᴇᴅ ꜰᴏʀ ɪᴅ #{user_id} \n•• ᴜꜱᴇʀɴᴀᴍᴇ : {username} \n\n•• ᖴᎥᒪᗴ Nᗩᗰᗴ : {fileName}",
        quote=True,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🚀 Fast Download 🚀", url=download),
             InlineKeyboardButton("🖥️ Watch online 🖥️", url=stream)]
        ])
    )

    msg_text = """<i><u>𝗬𝗼𝘂𝗿 𝗟𝗶𝗻𝗸 𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗲𝗱 !</u></i>\n\n<b>📂 Fɪʟᴇ ɴᴀᴍᴇ :</b> <i>{}</i>\n<b>📦 Fɪʟᴇ ꜱɪᴢᴇ :</b> <i>{}</i>\n<b>📥 Dᴏᴡɴʟᴏᴀᴅ :</b> <i>{}</i>\n<b>🖥 Wᴀᴛᴄʜ :</b> <i>{}</i>\n<b>🚸 Nᴏᴛᴇ : ʟɪɴᴋ ᴡᴏɴ'ᴛ ᴇxᴘɪʀᴇ ᴛɪʟʟ ɪ ᴅᴇʟᴇᴛᴇ</b>"""

    await message.reply_text(
        text=msg_text.format(
            get_name(log_msg),
            humanbytes(get_media_file_size(message)),
            download,
            stream
        ),
        quote=True,
        disable_web_page_preview=True
    )


# Show Plans Callback
@Client.on_callback_query(filters.regex("plans"))
async def show_plans_callback(client, callback_query):
    await callback_query.message.edit_text(
        text="""
<b>***ᴀᴠᴀɪʟᴀʙʟᴇ ᴘʟᴀɴs ♻️***</b>
<b>• 1 Week - ₹30 • 1 Month - ₹50 • 3 Months - ₹100 • 6 Months - ₹200</b>
<b>─────•─────────•─────•</b>
<b>***Premium Features 🎁***</b>
<b>○ No Captcha</b>
<b>○ Direct File Links</b>
<b>○ Ad-Free Experience</b>
<b>○ High-Speed Download</b>
<b>○ Unlimited Movies</b>
<b>○ Fast Support</b>
<b>○ Requests completed in 1 hour</b>
<b>─────•─────────•─────•</b>
<b>✨ UPI ID:</b> <code>lamasandeep821@okicici</code>
<b>📌 Check your active plan:</b> <code>/myplan</code>

<b>💢 Send screenshot after payment!</b>
""",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back", callback_data="back_to_home")]
        ]),
        parse_mode=enums.ParseMode.HTML,
        disable_web_page_preview=True
    )


# Back to Home Callback
@Client.on_callback_query(filters.regex("back_to_home"))
async def back_to_home_callback(client, callback_query):
    await callback_query.message.edit_text(
        text=script.START_TXT.format(callback_query.from_user.mention, temp.U_NAME, temp.B_NAME),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🎯 Show Plans", callback_data="plans")],
            [
                InlineKeyboardButton("♻️ Renew Premium", callback_data="renew"),
                InlineKeyboardButton("💳 Get Premium", callback_data="buy")
            ],
            [InlineKeyboardButton("📞 Contact Support", url="https://t.me/KingVJ01")]
        ]),
        parse_mode=enums.ParseMode.HTML
    )
