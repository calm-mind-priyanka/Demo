import datetime
import json
from info import PREMIUM_USERS, PREMIUM_DAYS

PREMIUM_JSON_FILE = "premium.json"

# Track daily usage per user
DAILY_USAGE = {}

# Helper: Save PREMIUM_USERS dict back to premium.json
def save_premium_users():
    to_save = {str(user): expiry.isoformat() for user, expiry in PREMIUM_USERS.items()}
    with open(PREMIUM_JSON_FILE, "w") as f:
        json.dump(to_save, f, indent=4)

# Convert PREMIUM_USERS expiry strings to datetime objects on load
def parse_premium_dates():
    for user, expiry_str in list(PREMIUM_USERS.items()):
        if isinstance(expiry_str, str):
            try:
                PREMIUM_USERS[user] = datetime.datetime.fromisoformat(expiry_str)
            except Exception:
                PREMIUM_USERS.pop(user)

# Call once on import
parse_premium_dates()

async def is_premium(user_id):
    if user_id not in PREMIUM_USERS:
        return False
    expiry_date = PREMIUM_USERS[user_id]
    return datetime.datetime.now() < expiry_date

def add_premium(user_id, days):
    expiry = datetime.datetime.now() + datetime.timedelta(days=days)
    PREMIUM_USERS[user_id] = expiry
    PREMIUM_DAYS[user_id] = days
    save_premium_users()
    parse_premium_dates()  # ✅ This line is the FIX

def remove_premium(user_id):
    PREMIUM_USERS.pop(user_id, None)
    PREMIUM_DAYS.pop(user_id, None)
    save_premium_users()
    parse_premium_dates()  # ✅ Keep it consistent

# ---- Daily limit for free users ----
def is_limited_today(user_id):
    today = datetime.date.today()
    if user_id in DAILY_USAGE and DAILY_USAGE[user_id]['date'] == today:
        return DAILY_USAGE[user_id]['used']
    return False

def mark_usage(user_id):
    today = datetime.date.today()
    DAILY_USAGE[user_id] = {'date': today, 'used': True}
