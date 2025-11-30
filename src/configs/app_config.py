from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """The application settings for me not for you"""

    # The logging home directory
    LOGS_DIR: str = "src/logs/"

    # Langfuse Configuration
    LANGFUSE_SECRET_KEY: str
    LANGFUSE_PUBLIC_KEY: str
    LANGFUSE_BASE_URL: str = "https://cloud.langfuse.com"

    # QA Agent Configuration
    QA_MODEL: str = "openrouter/openai/gpt-4o-mini"
    QA_TEMPERATURE: float = 0.2

    # OpenRouter API Key
    OPENROUTER_API_KEY: str


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """
        Returns an instance of the application settings class.
    """
    return Settings()
