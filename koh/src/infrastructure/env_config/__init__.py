import os
import platform
from decouple import Config, RepositoryEnv

os_paths = {
    "Darwin": "/",
    "Linux": "/",
    "Windows": "C:/",
}


def get_config() -> Config:
    system = platform.system()
    base_path = os_paths.get(system)
    if not base_path:
        raise Exception("Unsupported system")
    path = os.path.join(base_path, "opt", "envs", "koh.lionx.com.br", ".env")
    path = str(path)
    return Config(RepositoryEnv(path))


config = get_config()

__all__ = ["config"]
