import random
import humanize
from Script import script
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply, CallbackQuery
from info import URL, LOG_CHANNEL, SHORTLINK
from urllib.parse import quote_plus
from TechVJ.util.file_properties import get_name, get_hash, get_media_file_size
from TechVJ.util.human_readable import humanbytes
from database.users_chats_db import db
from utils import temp, get_shortlink

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
    return


@Client.on_message(filters.private & (filters.document | filters.video))
async def stream_start(client, message):
    file = getattr(message, message.media.value)
    filename = file.file_name
    filesize = humanize.naturalsize(file.file_size) 
    fileid = file.file_id
    user_id = message.from_user.id
    username = message.from_user.mention

    log_msg = await client.send_cached_media(
        chat_id=LOG_CHANNEL,
        file_id=fileid,
    )

    fileName = {quote_plus(get_name(log_msg))}

    if SHORTLINK == False:
        stream = f"{URL}watch/{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
        download = f"{URL}{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
    else:
        stream = await get_shortlink(
            f"{URL}watch/{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
        )
        download = await get_shortlink(
            f"{URL}{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
        )

    await log_msg.reply_text(
        text=f"•• ʟɪɴᴋ ɢᴇɴᴇʀᴀᴛᴇᴅ ꜰᴏʀ ɪᴅ #{user_id} \n•• ᴜꜱᴇʀɴᴀᴍᴇ : {username} \n\n•• ᖴᎥᒪᗴ Nᗩᗰᗴ : {fileName}",
        quote=True,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🚀 Fast Download 🚀", url=download),
             InlineKeyboardButton("🖥️ Watch online 🖥️", url=stream)]
        ])
    )

    rm = InlineKeyboardMarkup([
        [InlineKeyboardButton("sᴛʀᴇᴀᴍ 🖥", url=stream),
         InlineKeyboardButton("ᴅᴏᴡɴʟᴏᴀᴅ 📥", url=download)]
    ])

    msg_text = """<i><u>𝗬𝗼𝘂𝗿 𝗟𝗶𝗻𝗸 𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗲𝗱 !</u></i>\n\n<b>📂 Fɪʟᴇ ɴᴀᴍᴇ :</b> <i>{}</i>\n\n<b>📦 Fɪʟᴇ ꜱɪᴢᴇ :</b> <i>{}</i>\n\n<b>📥 Dᴏᴡɴʟᴏᴀᴅ :</b> <i>{}</i>\n\n<b> 🖥ᴡᴀᴛᴄʜ :</b> <i>{}</i>\n\n<b>🚸 Nᴏᴛᴇ : ʟɪɴᴋ ᴡᴏɴ'ᴛ ᴇxᴘɪʀᴇ ᴛɪʟʟ ɪ ᴅᴇʟᴇᴛᴇ</b>"""

    await message.reply_text(
        text=msg_text.format(
            get_name(log_msg),
            humanbytes(get_media_file_size(message)),
            download,
            stream
        ),
        quote=True,
        disable_web_page_preview=True,
        reply_markup=rm
    )


# ⬇️ Add this below your other handlers — Do not change any existing code

@Client.on_callback_query(filters.regex("plans"))
async def show_plans_callback(client, callback_query):
    await callback_query.message.edit_photo(
        photo="https://graph.org/file/5635f6bd5f76da19ccc70-695af75bfa01aacbf2.jpg",  # your QR image
        caption="""
<b>***ᴀᴠᴀɪʟᴀʙʟᴇ ᴘʟᴀɴs ♻️***</b>
<b>• 𝟷 ᴡᴇᴇᴋ - ₹𝟹𝟶 • 𝟷 ᴍᴏɴᴛʜ - ₹𝟻𝟶 • 𝟹 ᴍᴏɴᴛʜs - ₹𝟷𝟶𝟶 • 𝟼 ᴍᴏɴᴛʜs - ₹𝟸𝟶𝟶</b>
<b>─────•─────────•─────•</b>
<b>***ᴘʀᴇᴍɪᴜᴍ ꜰᴇᴀᴛᴜʀᴇs 🎁***</b>
<b>○ ɴᴏ ɴᴇᴇᴅ ᴛᴏ ᴠᴇʀɪꜰʏ
○ ᴅɪʀᴇᴄᴛ ꜰɪʟᴇs
○ ᴀᴅ-ꜰʀᴇᴇ ᴇxᴘᴇʀɪᴇɴᴄᴇ
○ ʜɪɢʜ-sᴘᴇᴇᴅ ᴅᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋ
○ ᴍᴜʟᴛɪ-ᴘʟᴀʏᴇʀ sᴛʀᴇᴀᴍɪɴɢ ʟɪɴᴋs
○ ᴜɴʟɪᴍɪᴛᴇᴅ ᴍᴏᴠɪᴇꜱ, ꜱᴇʀɪᴇꜱ & ᴀɴɪᴍᴇ
○ ꜰᴜʟʟ ᴀᴅᴍɪɴ sᴜᴘᴘᴏʀᴛ
○ ʀᴇǫᴜᴇsᴛ ᴡɪʟʟ ʙᴇ ᴄᴏᴍᴘʟᴇᴛᴇᴅ ɪɴ 𝟷ʜ</b>
<b>─────•─────────•─────•</b>
<b>✨ ᴜᴘɪ ɪᴅ -</b> <code>lamasandeep821@okicici</code>
<b>📌 ᴄʜᴇᴄᴋ ʏᴏᴜʀ ᴀᴄᴛɪᴠᴇ ᴘʟᴀɴ :</b> <code>/myplan</code>

<b>💢 ᴍᴜsᴛ sᴇɴᴅ sᴄʀᴇᴇɴsʜᴏᴛ ᴀꜰᴛᴇʀ ᴘᴀʏᴍᴇɴᴛ‼️ 
ᴀꜰᴛᴇʀ sᴇɴᴅɪɴɢ ᴀ sᴄʀᴇᴇɴsʜᴏᴛ ᴘʟᴇᴀsᴇ ɢɪᴠᴇ ᴍᴇ sᴏᴍᴇ ᴛɪᴍᴇ ᴛᴏ ᴀᴅᴅ ʏᴏᴜ ɪɴ ᴛʜᴇ ᴘʀᴇᴍɪᴜᴍ ᴠᴇʀsɪᴏɴ.</b>
""",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back", callback_data="back_to_home")]
        ]),
        parse_mode=enums.ParseMode.HTML
    )


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
