import datetime
import json
import os
from info import PREMIUM_USERS, PREMIUM_DAYS

PREMIUM_JSON_FILE = "premium.json"
USAGE_JSON_FILE = "usage.json"

# Track daily usage per user
if os.path.exists(USAGE_JSON_FILE):
    with open(USAGE_JSON_FILE) as f:
        DAILY_USAGE = json.load(f)
else:
    DAILY_USAGE = {}

# Save PREMIUM_USERS dict back to premium.json
def save_premium_users():
    to_save = {str(user): expiry.isoformat() for user, expiry in PREMIUM_USERS.items()}
    with open(PREMIUM_JSON_FILE, "w") as f:
        json.dump(to_save, f, indent=4)

# Convert PREMIUM_USERS expiry strings to datetime objects
def parse_premium_dates():
    for user, expiry_str in list(PREMIUM_USERS.items()):
        if isinstance(expiry_str, str):
            try:
                PREMIUM_USERS[user] = datetime.datetime.fromisoformat(expiry_str)
            except Exception:
                PREMIUM_USERS.pop(user)

# Call once at import
parse_premium_dates()

# Check if user is premium
async def is_premium(user_id):
    if user_id not in PREMIUM_USERS:
        return False
    expiry_date = PREMIUM_USERS[user_id]
    return datetime.datetime.now() < expiry_date

# Add premium to a user
def add_premium(user_id, days):
    expiry = datetime.datetime.now() + datetime.timedelta(days=days)
    PREMIUM_USERS[user_id] = expiry
    PREMIUM_DAYS[user_id] = days
    save_premium_users()
    parse_premium_dates()

# Remove premium from a user
def remove_premium(user_id):
    PREMIUM_USERS.pop(user_id, None)
    PREMIUM_DAYS.pop(user_id, None)
    save_premium_users()
    parse_premium_dates()

# Check if free user has already used bot today
def is_limited_today(user_id):
    today = datetime.date.today().isoformat()
    return DAILY_USAGE.get(str(user_id)) == today

# Mark that a free user has used bot today
def mark_usage(user_id):
    today = datetime.date.today().isoformat()
    DAILY_USAGE[str(user_id)] = today
    with open(USAGE_JSON_FILE, "w") as f:
        json.dump(DAILY_USAGE, f, indent=4)

# Load usage.json manually if needed
def load_usage():
    try:
        with open(USAGE_JSON_FILE, "r") as f:
            return json.load(f)
    except:
        return {}
