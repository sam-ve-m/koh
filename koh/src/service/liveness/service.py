import asyncio
from datetime import datetime

from etria_logger import Gladsheim
from jwt import jwk_from_pem, JWT

from koh.src.domain.exceptions.service.exceptions import UserNotFound
from koh.src.repository.files.repository import FileRepository
from koh.src.repository.cache.repository import CacheRepository
from koh.src.repository.user.repository import UserRepository
from koh.src.transport.unico.transport import UnicoTransport
from koh.src.infrastructure.env_config import config


class Liveness:
    jwt = JWT()

    @classmethod
    async def validate(cls, unique_id: str, selfie: str, feature: str) -> bool:
        if await cls._is_liveness_required(unique_id, feature) is False:
            Gladsheim.warning(
                "Liveness validation skipped",
                unique_id=unique_id,
                feature=feature,
            )
            return True
        elif not selfie:
            return False
        future_cpf = cls._get_user_cpf(unique_id)
        future_token = cls._get_token()
        cpf, token = await asyncio.gather(future_cpf, future_token)
        liveness_approved = await UnicoTransport.request_liveness_validation(
            selfie=selfie,
            token=token,
            cpf=cpf,
        )
        return liveness_approved

    cache_key = "token"

    @classmethod
    async def _get_token(cls):
        if not (token := await CacheRepository.get(cls.cache_key)):
            jwt = await cls._generate_jwt()
            token = await UnicoTransport.request_new_token(jwt)
            await CacheRepository.set(cls.cache_key, token, ttl=int(config("KOH_UNICO_TOKEN_TTL")))
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
        cpf = await UserRepository.get_user_cpf(unique_id)
        if not cpf:
            raise UserNotFound()
        return cpf

    @staticmethod
    async def _is_liveness_required(unique_id: str, feature: str) -> bool:
        key = ":".join(("bypass", unique_id, feature))
        if by_pass := await CacheRepository.get(key):
            by_pass = eval(by_pass)
        return not by_pass

