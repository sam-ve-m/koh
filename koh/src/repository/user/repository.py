from typing import Optional
from koh.src.infrastructure.env_config import config
from koh.src.infrastructure.mongo_db.infraestructure import MongoDBInfrastructure


class UserRepository:
    collection = None

    @classmethod
    def _get_collection(cls):
        if cls.collection is None:
            client = MongoDBInfrastructure.get_client()
            database = client[config("KOH_MONGODB_DATABASE_NAME")]
            cls.collection = database[config("KOH_MONGODB_USER_COLLECTION")]
        return cls.collection

    @classmethod
    async def _find_one(
        cls, query: dict, project: dict
    ) -> Optional[dict]:
        collection = cls._get_collection()
        data = await collection.find_one(query, project)
        return data

    @classmethod
    async def get_user_cpf(cls, unique_id: str) -> str:
        if user_cpf := await cls._find_one(
            query={"unique_id": unique_id},
            project={"identifier_document.cpf": 1, "_id": 0}
        ):
            user_cpf = user_cpf.get("identifier_document").get("cpf")
        return user_cpf
