import datetime
from info import ADMINS
from database.users_chats_db import db
from database.usage_db import UsageDB  # This should be defined in your usage_tracker.py

usage_db = UsageDB()

async def is_premium(user_id: int) -> bool:
    return user_id in ADMINS  # You can modify this to check from DB if you want dynamic premium list

async def can_generate_link(user_id: int) -> bool:
    if await is_premium(user_id):
        return True

    last_use = await usage_db.get_last_usage(user_id)
    if not last_use:
        await usage_db.update_usage(user_id)
        return True

    now = datetime.datetime.now()
    if (now - last_use).days >= 1:
        await usage_db.update_usage(user_id)
        return True

    return False
