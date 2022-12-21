from aioboto3 import Session
from contextlib import asynccontextmanager
from koh.src.infrastructure.env_config import config


class S3Infrastructure:
    session = None

    @classmethod
    async def _get_session(cls):
        if cls.session is None:
            cls.session = Session(
                aws_access_key_id=config("KOH_AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=config("KOH_AWS_SECRET_ACCESS_KEY"),
                region_name=config("KOH_AWS_REGION_NAME"),
            )
        return cls.session

    @classmethod
    @asynccontextmanager
    async def get_client(cls):
        session = await S3Infrastructure._get_session()
        async with session.client("s3") as s3_client:
            yield s3_client
