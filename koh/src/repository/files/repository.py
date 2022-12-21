from etria_logger import Gladsheim

from koh.src.domain.exceptions.repository.exceptions import PrivateKeyNotFound
from koh.src.infrastructure.http.infrastructure import HttpInfrastructure
from koh.src.infrastructure.s3.infrastructure import S3Infrastructure
from koh.src.infrastructure.env_config import config


class FileRepository:

    @classmethod
    async def _generate_file_link(cls, file_path: str) -> str:
        async with S3Infrastructure.get_client() as s3_client:
            link = await s3_client.generate_presigned_url(
                "get_object",
                Params={
                    "Bucket": config("KOH_AWS_FILE_BUCKET_NAME"),
                    "Key": file_path,
                },
                ExpiresIn=60,
            )
            return link

    @classmethod
    async def get_file(cls, file_path: str) -> bytes:
        file_link = await cls._generate_file_link(file_path)
        client = HttpInfrastructure.get_client()
        try:
            response = await client.get(file_link)
            file = await response.content.read()
            return file
        except Exception as error:
            Gladsheim.error(
                error=error,
                file_path=file_path,
                message=PrivateKeyNotFound.message
            )
            raise PrivateKeyNotFound()
