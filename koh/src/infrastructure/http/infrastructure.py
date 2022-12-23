from aiohttp import ClientSession


class HttpInfrastructure:
    client: ClientSession = None

    @classmethod
    def get_client(cls) -> ClientSession:
        if not cls.client:
            cls.client = ClientSession()
        return cls.client
