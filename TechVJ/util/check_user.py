from info import PREMIUM_USERS
from database.usage_db import UsageDB

async def can_generate_link(user_id: int) -> bool:
    if user_id in PREMIUM_USERS:
        return True
    return UsageDB.can_generate(user_id)

def increment_usage(user_id: int):
    if user_id not in PREMIUM_USERS:
        UsageDB.increment_usage(user_id)
