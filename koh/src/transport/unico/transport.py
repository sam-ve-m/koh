import json

from etria_logger import Gladsheim

from koh.src.domain.exceptions.transport.exceptions import UnmappedUnicoBehaviorError
from koh.src.infrastructure.http.infrastructure import HttpInfrastructure
from koh.src.infrastructure.env_config import config


class UnicoTransport:
    @staticmethod
    async def _post(url, **kwargs) -> dict:
        http_session = HttpInfrastructure.get_client()
        try:
            response = await http_session.post(url, **kwargs)
            response_text = await response.text()
            if not response.ok:
                Gladsheim.error(
                    message="Not success response received",
                    response=response_text,
                    args=kwargs,
                    url=url,
                )
            response_json = json.loads(response_text)
            return response_json
        except Exception as error:
            Gladsheim.error(
                error=error,
                url=url,
                args=kwargs
            )
            raise UnmappedUnicoBehaviorError()

    @classmethod
    async def request_new_token(cls, jwt: str) -> str:
        url = config("KOH_UNICO_URL_GENERATE_TOKEN")
        body = {
            "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
            "assertion": jwt,
        }
        response_json = await cls._post(url, data=body)
        token = response_json.get("access_token")
        if not token:
            Gladsheim.error(
                message=UnmappedUnicoBehaviorError.message,
                json=response_json,
            )
            raise UnmappedUnicoBehaviorError()
        return token

    @staticmethod
    def _get_headers(token: str) -> dict:
        api_key = config("KOH_UNICO_API_KEY")
        headers = {"APIKEY": api_key, "Authorization": token}
        return headers

    @classmethod
    async def request_liveness_validation(
        cls, selfie: str, cpf: str, token: str
    ) -> bool:
        url = config("KOH_UNICO_URL_LIVENESS")
        body = {"code": cpf, "imagebase64": selfie}
        headers = cls._get_headers(token)
        response_json = await cls._post(url, headers=headers, json=body)
        liveness_status = response_json.get("Status")
        if liveness_status is None:
            Gladsheim.error(
                message=UnmappedUnicoBehaviorError.message,
                json=response_json,
            )
            raise UnmappedUnicoBehaviorError()
        return liveness_status
