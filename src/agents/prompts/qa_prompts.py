from langchain_core.messages import SystemMessage
from functools import lru_cache
from src.configs import setup_logger

class QAPrompts:
    """Quality Assurance Prompts"""

    @staticmethod
    @lru_cache(maxsize=1)
    def get_system_prompt() -> SystemMessage:
        prompt = """
You are a professional quality assurance agent.

"""

        logger = setup_logger(logger_name=__name__, level="info")
        logger.info("System prompt retreived successfully.")
        return SystemMessage(content=prompt.format())
