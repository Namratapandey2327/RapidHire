from pymongo import MongoClient
from typing import Optional

class MongoDBClient:
    """MongoDB wrapper for SourceSync storage."""

    def __init__(self, uri: str, database: str = "sourcesync"):
        self.client = MongoClient(uri)
        self.db = self.client[database]

    def get_collection(self, name: str):
        return self.db[name]

    def close(self):
        self.client.close()
