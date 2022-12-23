from koh.src.domain.enum.status.enum import KohStatus
from koh.src.domain.exceptions.exception import KohException


class UnmappedUnicoBehaviorError(KohException):
    message = "Something unexpected returned from Unico"
    status = KohStatus.UNEXPECTED_BEHAVIOR
