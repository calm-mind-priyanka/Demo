import datetime
import json
import os
from info import PREMIUM_USERS, PREMIUM_DAYS

PREMIUM_JSON_FILE = "premium.json"
USAGE_JSON_FILE = "usage.json"

# Initialize usage dict
DAILY_USAGE = {}

# Load usage data from file
def load_usage():
    global DAILY_USAGE
    if os.path.exists(USAGE_JSON_FILE):
        try:
            with open(USAGE_JSON_FILE, "r") as f:
                DAILY_USAGE = json.load(f)
        except:
            DAILY_USAGE = {}
    else:
        DAILY_USAGE = {}

load_usage()

# Save PREMIUM_USERS to file
def save_premium_users():
    with open(PREMIUM_JSON_FILE, "w") as f:
        json.dump({str(user): expiry.isoformat() for user, expiry in PREMIUM_USERS.items()}, f, indent=4)

# Parse expiry strings to datetime
def parse_premium_dates():
    for user, expiry_str in list(PREMIUM_USERS.items()):
        if isinstance(expiry_str, str):
            try:
                PREMIUM_USERS[user] = datetime.datetime.fromisoformat(expiry_str)
            except:
                PREMIUM_USERS.pop(user)

parse_premium_dates()

# Check if user is premium
async def is_premium(user_id):
    expiry = PREMIUM_USERS.get(str(user_id)) or PREMIUM_USERS.get(user_id)
    if not expiry:
        return False
    if isinstance(expiry, str):
        try:
            expiry = datetime.datetime.fromisoformat(expiry)
        except:
            return False
    return datetime.datetime.now() < expiry

# Add premium
def add_premium(user_id, days):
    expiry = datetime.datetime.now() + datetime.timedelta(days=days)
    PREMIUM_USERS[str(user_id)] = expiry
    PREMIUM_DAYS[str(user_id)] = days
    save_premium_users()
    parse_premium_dates()

# Remove premium
def remove_premium(user_id):
    PREMIUM_USERS.pop(str(user_id), None)
    PREMIUM_DAYS.pop(str(user_id), None)
    save_premium_users()

# Has used today (for free users)
def is_limited_today(user_id):
    today = datetime.date.today().isoformat()
    return DAILY_USAGE.get(str(user_id)) == today

# Mark that user used today
def mark_usage(user_id):
    today = datetime.date.today().isoformat()
    DAILY_USAGE[str(user_id)] = today
    with open(USAGE_JSON_FILE, "w") as f:
        json.dump(DAILY_USAGE, f, indent=4)
