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
        # Don't connect immediately - lazy loading
        pass
    
    def _connect(self):
        """Lazy connection to MongoDB"""
        if self._client is None:
            try:
                self._client = MongoClient(
                    Config.MONGODB_URI,
                    serverSelectionTimeoutMS=5000,
                    connectTimeoutMS=10000,
                    socketTimeoutMS=10000,
                    retryWrites=True,
                    tlsAllowInvalidCertificates=False
                )
                self._db = self._client[Config.MONGODB_DB_NAME]
                # Test connection
                self._client.admin.command('ping')
                print("✅ MongoDB connected successfully")
                self._setup_indexes()
            except Exception as e:
                print(f"❌ MongoDB connection error: {e}")
                # Don't fail - let app start without DB
                self._client = None
                self._db = None
    
    def _setup_indexes(self):
        """Create indexes for better query performance"""
        try:
            if self._db is not None:
                self._db.emails.create_index([('user_email', ASCENDING), ('gmail_id', ASCENDING)], unique=True)
                self._db.emails.create_index([('user_email', ASCENDING), ('date', DESCENDING)])
                self._db.emails.create_index([('user_email', ASCENDING), ('status', ASCENDING)])
                print("✅ MongoDB indexes created")
        except Exception as e:
            print(f"⚠️  Index creation warning: {e}")
    
    @property
    def emails(self):
        if self._client is None:
            self._connect()
        return self._db.emails if self._db else None
    
    @property
    def users(self):
        if self._client is None:
            self._connect()
        return self._db.users if self._db else None
    
    def close(self):
        if self._client:
            self._client.close()

# Create a single database instance
db = Database()