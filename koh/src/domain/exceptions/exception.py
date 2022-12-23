from koh.src.domain.enum.status.enum import KohStatus


class KohException(Exception):
    status: KohStatus
    message: str
