# database/users_chats_db.py

import motor.motor_asyncio
from info import DATABASE_NAME, DATABASE_URI
from datetime import datetime

class Database:

    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users

    def new_user(self, id, name):
        return dict(
            id=id,
            name=name,
            premium=False,
            expiry=None
        )

    async def add_user(self, id, name):
        user = self.new_user(id, name)
        if not await self.is_user_exist(id):
            await self.col.insert_one(user)

    async def is_user_exist(self, id):
        user = await self.col.find_one({'id': int(id)})
        return bool(user)

    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count

    async def get_all_users(self):
        return self.col.find({})

    async def delete_user(self, user_id):
        await self.col.delete_many({'id': int(user_id)})

    # PREMIUM FUNCTIONS BELOW

    async def add_premium(self, user_id, expiry_date):
        await self.col.update_one(
            {'id': int(user_id)},
            {'$set': {'premium': True, 'expiry': expiry_date}},
            upsert=True
        )

    async def remove_premium(self, user_id):
        await self.col.update_one(
            {'id': int(user_id)},
            {'$set': {'premium': False, 'expiry': None}}
        )

    async def is_premium(self, user_id):
        user = await self.col.find_one({'id': int(user_id)})
        if user and user.get("premium") and user.get("expiry"):
            expiry = user["expiry"]
            if isinstance(expiry, datetime) and expiry > datetime.utcnow():
                return True, expiry
            else:
                # Expired, auto-remove premium
                await self.remove_premium(user_id)
        return False, None

# Create db instance
db = Database(DATABASE_URI, DATABASE_NAME)
