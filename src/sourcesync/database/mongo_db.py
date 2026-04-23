from pymongo import MongoClient
from typing import Optional
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class MongoDBClient:
    """MongoDB wrapper for SourceSync storage."""

    def __init__(self, uri: str, database: str = "sourcesync"):
        self.client = MongoClient(uri)
        self.db = self.client[database]

    def get_collection(self, name: str):
        return self.db[name]

    def close(self):
        self.client.close()

    # User management methods
    def insert_user(self, email: str, hashed_password: str) -> str:
        """Insert a new user and return the inserted ID."""
        users = self.get_collection("users")
        result = users.insert_one({"email": email, "password": hashed_password})
        return str(result.inserted_id)

    def get_user_by_email(self, email: str) -> Optional[dict]:
        """Get user by email."""
        users = self.get_collection("users")
        return users.find_one({"email": email})

    def hash_password(self, password: str) -> str:
        """Hash a password."""
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        return pwd_context.verify(plain_password, hashed_password)
