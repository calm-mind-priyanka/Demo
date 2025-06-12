import datetime

class UsageDB:
    usage_data = {}

    @classmethod
    def can_generate(cls, user_id):
        today = datetime.date.today().isoformat()
        user_data = cls.usage_data.get(user_id, {})
        if user_data.get("date") != today:
            cls.usage_data[user_id] = {"date": today, "count": 0}
        return cls.usage_data[user_id]["count"] < 1

    @classmethod
    def increment_usage(cls, user_id):
        today = datetime.date.today().isoformat()
        if user_id not in cls.usage_data or cls.usage_data[user_id]["date"] != today:
            cls.usage_data[user_id] = {"date": today, "count": 1}
        else:
            cls.usage_data[user_id]["count"] += 1
