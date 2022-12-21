from koh.src.domain.enum.status.enum import KohStatus
from koh.src.domain.exceptions.exception import KohException


class PrivateKeyNotFound(KohException):
    message = "Unable to find private key to login in Unico"
    status = KohStatus.UNEXPECTED_BEHAVIOR
