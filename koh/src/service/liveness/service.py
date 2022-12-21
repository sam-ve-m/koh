import asyncio
from datetime import datetime

from jwt import jwk_from_pem, JWT

from koh.src.repository.files.repository import FileRepository
from koh.src.repository.cache.repository import CacheRepository
from koh.src.repository.user.repository import UserRepository
from koh.src.transport.unico.transport import UnicoTransport
from koh.src.infrastructure.env_config import config


class Liveness:
    jwt = JWT()

    @classmethod
    async def validate(cls, selfie: str, unique_id: str) -> bool:
        future_token = cls._get_token()
        future_cpf = cls._get_user_cpf(unique_id)
        cpf, token = await asyncio.gather(future_cpf, future_token)
        liveness_approved = await UnicoTransport.request_liveness_validation(
            selfie=selfie,
            token=token,
            cpf=cpf,
        )
        return liveness_approved

    cache_key = "liveness:token"

    @classmethod
    async def _get_token(cls):
        if not (token := await CacheRepository.get(cls.cache_key)):
            jwt = await cls._generate_jwt()
            token = await UnicoTransport.request_new_token(jwt)
            await CacheRepository.set(cls.cache_key, token, ttl=3000)
        return token

    @classmethod
    async def _generate_jwt(cls) -> str:
        payload = cls._get_jwt_generation_payload()
        private_key = await cls._get_private_key()
        signing_key = jwk_from_pem(private_key)
        jwt = cls.jwt.encode(payload, key=signing_key, alg="RS256")
        return jwt

    @staticmethod
    def _get_jwt_generation_payload():
        now = datetime.utcnow().timestamp()
        payload = {
            "iss": config("KOH_UNICO_PARAM_JWT_GENERATION_ISS"),
            "aud": config("KOH_UNICO_PARAM_JWT_GENERATION_AUD"),
            "scope": config("KOH_UNICO_PARAM_JWT_GENERATION_SCOPE"),
            "iat": now,
            "exp": now + int(config("KOH_UNICO_PARAM_EXPIRATION")),
        }
        return payload

    @staticmethod
    async def _get_private_key() -> bytes:
        file_path = config("KOH_UNICO_FILE_PATH_PRIVATE_KEY")
        private_key = await FileRepository.get_file(file_path)
        return private_key

    @staticmethod
    async def _get_user_cpf(unique_id: str) -> str:
        cache_key = ":".join(("unique_id_to_cpf", unique_id))
        if not (cpf := await CacheRepository.get(cache_key)):
            cpf = await UserRepository.get_user_cpf(unique_id)
            ttl = int(config("KOH_UNIQUE_ID_TO_CPF_MAP_TTL"))
            await CacheRepository.set(cache_key, cpf, ttl=ttl)
        return cpf
