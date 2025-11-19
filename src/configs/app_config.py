from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """The application settings for me not for you"""

    # The logging home directory
    LOGS_DIR: str = "src/logs/"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()