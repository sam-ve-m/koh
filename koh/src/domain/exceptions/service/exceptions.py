from koh.src.domain.enum.status.enum import KohStatus
from koh.src.domain.exceptions.exception import KohException


class UserNotFound(KohException):
    message = "Unable to user"
    status = KohStatus.UNEXPECTED_BEHAVIOR
