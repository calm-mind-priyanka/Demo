from info import PREMIUM_USERS, PREMIUM_DAYS
import datetime

# Track daily usage per user
DAILY_USAGE = {}

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

# ---- Daily limit for free users ----
def is_limited_today(user_id):
    today = datetime.date.today()
    if user_id in DAILY_USAGE and DAILY_USAGE[user_id]['date'] == today:
        return DAILY_USAGE[user_id]['used']
    return False

def mark_usage(user_id):
    today = datetime.date.today()
    DAILY_USAGE[user_id] = {'date': today, 'used': True}
