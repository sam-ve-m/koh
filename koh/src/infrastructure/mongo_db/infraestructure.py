from motor.motor_asyncio import AsyncIOMotorClient
from koh.src.infrastructure.env_config import config


class MongoDBInfrastructure:

    client = None

    @classmethod
    def get_client(cls):
        if cls.client is None:
            url = config("KOH_MONGO_CONNECTION_URL")
            cls.client = AsyncIOMotorClient(url)
        return cls.client
