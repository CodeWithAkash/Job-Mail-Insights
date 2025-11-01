from pymongo import MongoClient, ASCENDING, DESCENDING
from config import Config
from datetime import datetime

class Database:
    _instance = None
    _client = None
    _db = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._client is None:
            self._client = MongoClient(Config.MONGODB_URI)
            self._db = self._client[Config.MONGODB_DB_NAME]
            self._setup_indexes()
    
    def _setup_indexes(self):
        """Create indexes for better query performance"""
        self._db.emails.create_index([('user_email', ASCENDING), ('gmail_id', ASCENDING)], unique=True)
        self._db.emails.create_index([('user_email', ASCENDING), ('date', DESCENDING)])
        self._db.emails.create_index([('user_email', ASCENDING), ('status', ASCENDING)])
    
    @property
    def emails(self):
        return self._db.emails
    
    @property
    def users(self):
        return self._db.users
    
    def close(self):
        if self._client:
            self._client.close()

# Create a single database instance
db = Database()