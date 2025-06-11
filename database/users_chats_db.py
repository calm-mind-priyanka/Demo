import motor.motor_asyncio
from info import DATABASE_NAME, DATABASE_URI

class Database:

    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users

    def new_user(self, id, name):
        return dict(
            id = id,
            name = name,
            is_premium = False,           # 🔹 default is not premium
            daily_usage = {}              # 🔹 track per day usage
        )

    async def add_user(self, id, name):
        if not await self.is_user_exist(id):
            user = self.new_user(id, name)
            await self.col.insert_one(user)

    async def is_user_exist(self, id):
        user = await self.col.find_one({'id': int(id)})
        return bool(user)

    async def total_users_count(self):
        return await self.col.count_documents({})

    async def get_all_users(self):
        return self.col.find({})

    async def delete_user(self, user_id):
        await self.col.delete_many({'id': int(user_id)})

    # ✅ Check if user is premium
    async def is_premium(self, user_id: int) -> bool:
        user = await self.col.find_one({'id': int(user_id)})
        return user and user.get('is_premium', False)

    # ✅ Make user premium manually (for admin use)
    async def set_premium(self, user_id: int, status: bool = True):
        await self.col.update_one(
            {'id': int(user_id)},
            {'$set': {'is_premium': status}}
        )

    # ✅ Get daily file count
    async def get_daily_count(self, user_id: int, date: str) -> int:
        user = await self.col.find_one({'id': int(user_id)})
        if not user:
            return 0
        return user.get("daily_usage", {}).get(date, 0)

    # ✅ Increment daily file count
    async def increment_daily_count(self, user_id: int, date: str):
        await self.col.update_one(
            {'id': int(user_id)},
            {'$inc': {f'daily_usage.{date}': 1}},
            upsert=True
        )

db = Database(DATABASE_URI, DATABASE_NAME)
