from typing import Tuple

from etria_logger import Gladsheim
from koh.src.service.liveness.service import Liveness
from koh.src.domain.enum.status.enum import KohStatus
from koh.src.domain.exceptions.exception import KohException


class Koh:
    @staticmethod
    async def check_face(unique_id: str, face: str, feature: str) -> Tuple[bool, KohStatus]:
        try:
            status = await Liveness.validate(unique_id, face, feature)
            return status, KohStatus.SUCCESS
        except KohException as error:
            return False, error.status
        except Exception as error:
            Gladsheim.error(error, "Something went wrong")
            return False, KohStatus.UNEXPECTED_BEHAVIOR
