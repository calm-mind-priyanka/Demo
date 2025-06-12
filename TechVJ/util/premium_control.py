from info import PREMIUM_USERS, PREMIUM_DAYS
import datetime

def is_premium(user_id):
    if user_id not in PREMIUM_USERS:
        return False
    expiry_date = PREMIUM_USERS[user_id]
    return datetime.datetime.now() < expiry_date

def add_premium(user_id, days):
    expiry = datetime.datetime.now() + datetime.timedelta(days=days)
    PREMIUM_USERS[user_id] = expiry
    PREMIUM_DAYS[user_id] = days

def remove_premium(user_id):
    PREMIUM_USERS.pop(user_id, None)
    PREMIUM_DAYS.pop(user_id, None)
