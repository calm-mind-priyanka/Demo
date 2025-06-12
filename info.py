import re
from os import environ

id_pattern = re.compile(r'^.\d+$')

SESSION = environ.get('SESSION', 'TechVJBot')
API_ID = int(environ.get('API_ID', '24222039'))
API_HASH = environ.get('API_HASH', '6dd2dc70434b2f577f76a2e993135662')
BOT_TOKEN = environ.get('BOT_TOKEN', "")

PORT = environ.get("PORT", "8080")
MULTI_CLIENT = False
SLEEP_THRESHOLD = int(environ.get('SLEEP_THRESHOLD', '60'))
PING_INTERVAL = int(environ.get("PING_INTERVAL", "1200"))
ON_HEROKU = 'DYNO' in environ
URL = environ.get("URL", "")

LOG_CHANNEL = int(environ.get('LOG_CHANNEL', '-1002433610423'))
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('ADMINS', '6046055058').split()]
OWNER_ID = int(environ.get('OWNER_ID', '6046055058'))

DATABASE_URI = environ.get('DATABASE_URI', "mongodb+srv://Rpsing:Rpsing2003@rpsing.thqdyo6.mongodb.net/?retryWrites=true&w=majority&appName=Rpsing")
DATABASE_NAME = environ.get('DATABASE_NAME', "techvjautobot")

SHORTLINK = bool(environ.get('SHORTLINK', False))
SHORTLINK_URL = environ.get('SHORTLINK_URL', 'api.shareus.io')
SHORTLINK_API = environ.get('SHORTLINK_API', 'hRPS5vvZc0OGOEUQJMJzPiojoVK2')

PREMIUM_FILE = "premium_users.json"
USAGE_FILE = "daily_usage.json"
F_SUB_FILE = "force_sub_channels.json"
