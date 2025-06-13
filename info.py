import re
import json
import datetime
from os import environ

id_pattern = re.compile(r'^.\d+$')

# Bot Info
SESSION = environ.get('SESSION', 'TechVJBot')
API_ID = int(environ.get('API_ID', '24222039'))
API_HASH = environ.get('API_HASH', '6dd2dc70434b2f577f76a2e993135662')
BOT_TOKEN = environ.get('BOT_TOKEN', "")

# App Settings
PORT = environ.get("PORT", "8080")
MULTI_CLIENT = False
SLEEP_THRESHOLD = int(environ.get('SLEEP_THRESHOLD', '60'))
PING_INTERVAL = int(environ.get("PING_INTERVAL", "1200"))
ON_HEROKU = 'DYNO' in environ
URL = environ.get("URL", "")

# Admins & Logging
LOG_CHANNEL = int(environ.get('LOG_CHANNEL', '-1002433610423'))
ADMINS = [
    int(admin) if id_pattern.search(admin) else admin
    for admin in environ.get('ADMINS', '6046055058').split()
]

# MongoDB Config
DATABASE_URI = environ.get(
    'DATABASE_URI',
    "mongodb+srv://Rpsing:Rpsing2003@rpsing.thqdyo6.mongodb.net/?retryWrites=true&w=majority&appName=Rpsing"
)
DATABASE_NAME = environ.get('DATABASE_NAME', "techvjautobot")

# Shortlink Config
SHORTLINK = bool(environ.get('SHORTLINK', False))
SHORTLINK_URL = environ.get('SHORTLINK_URL', 'api.shareus.io')
SHORTLINK_API = environ.get('SHORTLINK_API', 'hRPS5vvZc0OGOEUQJMJzPiojoVK2')

# FSub Channels
try:
    with open("fsub.json", "r") as fs:
        FSUB_CHANNELS = json.load(fs)
except Exception:
    FSUB_CHANNELS = []

# Premium Users with expiry
try:
    with open("premium.json", "r") as pf:
        PREMIUM_USERS = json.load(pf)
        if not isinstance(PREMIUM_USERS, dict):
            print("[WARN] premium.json is not a dict. Resetting.")
            PREMIUM_USERS = {}
except Exception as e:
    print(f"[ERROR] Failed to load premium.json: {e}")
    PREMIUM_USERS = {}

# Optional: Keep track of how many days a user got
PREMIUM_DAYS = {}
