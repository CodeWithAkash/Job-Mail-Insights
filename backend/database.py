from pymongo import MongoClient, ASCENDING, DESCENDING
from config import Config

class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._connect()
        return cls._instance

    def _connect(self):
        try:
            self.client = MongoClient(
                Config.MONGODB_URI,
                serverSelectionTimeoutMS=5000
            )
            self.db = self.client[Config.MONGODB_DB_NAME]
            self.client.admin.command('ping')
            print("✅ MongoDB connected successfully")

            self._setup_indexes()

        except Exception as e:
            print(f"❌ MongoDB connection error: {e}")
            raise Exception("Database connection failed")

    def _setup_indexes(self):
        self.db.emails.create_index(
            [('user_email', ASCENDING), ('gmail_id', ASCENDING)],
            unique=True
        )
        self.db.emails.create_index(
            [('user_email', ASCENDING), ('date', DESCENDING)]
        )
        self.db.emails.create_index(
            [('user_email', ASCENDING), ('status', ASCENDING)]
        )
        print("✅ MongoDB indexes created")

    @property
    def emails(self):
        return self.db.emails

    @property
    def users(self):
        return self.db.users


db = Database()