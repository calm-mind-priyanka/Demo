import random
import humanize
from Script import script
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from info import URL, LOG_CHANNEL, SHORTLINK
from urllib.parse import quote_plus
from TechVJ.util.file_properties import get_name, get_hash, get_media_file_size
from TechVJ.util.human_readable import humanbytes
from database.users_chats_db import db
from utils import temp, get_shortlink

# Force sub & premium check import
from plugins.fsub import is_subscribed
from plugins.premium import is_premium


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


@Client.on_message(filters.private & (filters.document | filters.video))
async def stream_start(client, message):
    user_id = message.from_user.id
    username = message.from_user.mention

    # Force Sub Check
    if not await is_subscribed(client, user_id):
        await message.reply_text(
            "❌ You must join the update channel to use this bot.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📢 Join Channel", url="https://t.me/YOUR_CHANNEL_USERNAME")],
                [InlineKeyboardButton("✅ I've Joined", callback_data="checksub")]
            ])
        )
        return

    # Premium Check
    if not await is_premium(user_id):
        await message.reply_text(
            "🚫 You are not a Premium user.\n\n💳 To generate links, please upgrade to a premium plan.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💎 Buy Premium", callback_data="buy")],
                [InlineKeyboardButton("📞 Contact Support", url="https://t.me/KingVJ01")]
            ])
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

    file_name_encoded = quote_plus(get_name(log_msg))
    file_hash = get_hash(log_msg)

    if not SHORTLINK:
        stream = f"{URL}watch/{log_msg.id}/{file_name_encoded}?hash={file_hash}"
        download = f"{URL}{log_msg.id}/{file_name_encoded}?hash={file_hash}"
        embed = f"{URL}e/{log_msg.id}/{file_name_encoded}?hash={file_hash}"
    else:
        stream = await get_shortlink(f"{URL}watch/{log_msg.id}/{file_name_encoded}?hash={file_hash}")
        download = await get_shortlink(f"{URL}{log_msg.id}/{file_name_encoded}?hash={file_hash}")
        embed = await get_shortlink(f"{URL}e/{log_msg.id}/{file_name_encoded}?hash={file_hash}")

    await log_msg.reply_text(
        text=f"•• ʟɪɴᴋ ɢᴇɴᴇʀᴀᴛᴇᴅ ꜰᴏʀ ɪᴅ #{user_id} \n•• ᴜꜱᴇʀɴᴀᴍᴇ : {username} \n\n•• ᖴᎥᒪᗴ Nᗩᗰᗴ : {file_name_encoded}",
        quote=True,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🚀 Fast Download", url=download),
                InlineKeyboardButton("🖥️ Watch Online", url=stream)
            ],
            [InlineKeyboardButton("📺 Embed", url=embed)]
        ])
    )

    rm = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🖥 Stream", url=stream),
            InlineKeyboardButton("📥 Download", url=download)
        ],
        [InlineKeyboardButton("📺 Embed", url=embed)]
    ])

    msg_text = """<i><u>𝗬𝗼𝘂𝗿 𝗟𝗶𝗻𝗸 𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗲𝗱 !</u></i>\n\n<b>📂 Fɪʟᴇ ɴᴀᴍᴇ :</b> <i>{}</i>\n\n<b>📦 Fɪʟᴇ ꜱɪᴢᴇ :</b> <i>{}</i>\n\n<b>📥 Dᴏᴡɴʟᴏᴀᴅ :</b> <i>{}</i>\n\n<b>🖥 𝗪𝗮𝘁𝗰𝗵 :</b> <i>{}</i>\n\n<b>📺 𝗘𝗺𝗯𝗲𝗱 :</b> <i>{}</i>\n\n<b>🚸 Nᴏᴛᴇ : ʟɪɴᴋ ᴡᴏɴ'ᴛ ᴇxᴘɪʀᴇ ᴛɪʟʟ ɪ ᴅᴇʟᴇᴛᴇ</b>"""

    await message.reply_text(
        text=msg_text.format(
            get_name(log_msg),
            humanbytes(get_media_file_size(message)),
            download,
            stream,
            embed
        ),
        quote=True,
        disable_web_page_preview=True,
        reply_markup=rm
    )


@Client.on_callback_query(filters.regex("plans"))
async def show_plans_callback(client, callback_query):
    await callback_query.message.edit_text(
        text="""<your plans message here>""",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back", callback_data="back_to_home")]
        ]),
        parse_mode=enums.ParseMode.HTML,
        disable_web_page_preview=False
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
